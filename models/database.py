import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "testdrive.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


class DatabaseModel:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self._inicializar_banco()

    def _conectar(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _inicializar_banco(self) -> None:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        with self._conectar() as conn:
            conn.executescript(schema_sql)

    # --- VEÍCULOS ---
    def inserir_veiculo(self, modelo: str, versao: str, ano: int, placa: str, status: str = "Disponível") -> int:
        with self._conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO veiculos (modelo, versao, ano, placa, status) VALUES (?, ?, ?, ?, ?)",
                (modelo.strip(), versao.strip(), int(ano), placa.strip().upper(), status),
            )
            return cursor.lastrowid

    def listar_veiculos(self) -> list[dict]:
        with self._conectar() as conn:
            rows = conn.execute("SELECT * FROM veiculos ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    def buscar_veiculo_por_id(self, veiculo_id: int) -> dict | None:
        with self._conectar() as conn:
            row = conn.execute("SELECT * FROM veiculos WHERE id = ?", (veiculo_id,)).fetchone()
            return dict(row) if row else None

    def atualizar_status_veiculo(self, veiculo_id: int, novo_status: str) -> None:
        with self._conectar() as conn:
            conn.execute(
                "UPDATE veiculos SET status = ? WHERE id = ?",
                (novo_status, veiculo_id),
            )

    # --- CLIENTES ---
    def inserir_cliente(self, nome: str, cnh: str, telefone: str) -> int:
        with self._conectar() as conn:
            cursor = conn.execute(
                "INSERT INTO clientes (nome, cnh, telefone) VALUES (?, ?, ?)",
                (nome.strip(), cnh, telefone.strip()),
            )
            return cursor.lastrowid

    def listar_clientes(self) -> list[dict]:
        with self._conectar() as conn:
            rows = conn.execute("SELECT * FROM clientes ORDER BY id DESC").fetchall()
            return [dict(row) for row in rows]

    # --- AGENDAMENTOS ---
    def inserir_agendamento(self, veiculo_id: int, cliente_id: int, data_agendamento: str) -> int:
        with self._conectar() as conn:
            cursor = conn.execute(
                """
                INSERT INTO agendamentos (veiculo_id, cliente_id, data_agendamento, status)
                VALUES (?, ?, ?, 'Confirmado')
                """,
                (veiculo_id, cliente_id, data_agendamento),
            )
            conn.execute(
                "UPDATE veiculos SET status = 'Agendado' WHERE id = ?",
                (veiculo_id,),
            )
            return cursor.lastrowid

    def listar_agendamentos(self) -> list[dict]:
        query = """
            SELECT 
                a.id,
                a.veiculo_id,
                v.modelo || ' ' || v.versao AS veiculo,
                v.placa,
                c.nome AS cliente,
                c.cnh,
                a.data_agendamento,
                a.status
            FROM agendamentos a
            JOIN veiculos v ON a.veiculo_id = v.id
            JOIN clientes c ON a.cliente_id = c.id
            ORDER BY a.id DESC
        """
        with self._conectar() as conn:
            rows = conn.execute(query).fetchall()
            return [dict(row) for row in rows]

    def buscar_agendamento_por_id(self, agendamento_id: int) -> dict | None:
        with self._conectar() as conn:
            row = conn.execute("SELECT * FROM agendamentos WHERE id = ?", (agendamento_id,)).fetchone()
            return dict(row) if row else None

    def atualizar_status_agendamento(self, agendamento_id: int, novo_status: str) -> None:
        agendamento = self.buscar_agendamento_por_id(agendamento_id)
        if not agendamento:
            raise ValueError("Agendamento não encontrado.")

        with self._conectar() as conn:
            conn.execute(
                "UPDATE agendamentos SET status = ? WHERE id = ?",
                (novo_status, agendamento_id),
            )
            if novo_status in ("Concluído", "Cancelado"):
                conn.execute(
                    "UPDATE veiculos SET status = 'Disponível' WHERE id = ?",
                    (agendamento["veiculo_id"],),
                )