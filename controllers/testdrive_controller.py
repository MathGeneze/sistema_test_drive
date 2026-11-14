import re
import sqlite3
from datetime import date
from models.database import DatabaseModel


class TestDriveController:
    def __init__(self, db: DatabaseModel | None = None):
        self.db = db or DatabaseModel()

    # --- REGRAS DE VEÍCULOS ---
    def cadastrar_veiculo(self, modelo: str, versao: str, ano: int, placa: str) -> int:
        if not modelo.strip() or not versao.strip() or not placa.strip():
            raise ValueError("Modelo, versão e placa são obrigatórios.")
        placa_limpa = re.sub(r"[^A-Za-z0-9]", "", placa).upper()
        if len(placa_limpa) != 7:
            raise ValueError("A placa deve conter exatamente 7 caracteres alfanuméricos.")
        try:
            return self.db.inserir_veiculo(modelo, versao, ano, placa_limpa)
        except sqlite3.IntegrityError:
            raise ValueError(f"Já existe um veículo cadastrado com a placa {placa_limpa}.")

    def listar_veiculos(self) -> list[dict]:
        return self.db.listar_veiculos()

    def alterar_status_veiculo(self, veiculo_id: int, novo_status: str) -> None:
        if novo_status not in ("Disponível", "Agendado", "Em Manutenção"):
            raise ValueError("Status de veículo inválido.")
        veiculo = self.db.buscar_veiculo_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veículo não encontrado.")
        self.db.atualizar_status_veiculo(veiculo_id, novo_status)

    # --- REGRAS DE CLIENTES ---
    def cadastrar_cliente(self, nome: str, cnh: str, telefone: str) -> int:
        if not nome.strip() or not telefone.strip():
            raise ValueError("Nome e telefone são obrigatórios.")
        cnh_numerica = re.sub(r"\D", "", cnh)
        if len(cnh_numerica) != 11:
            raise ValueError("A CNH deve conter exatamente 11 dígitos numéricos.")
        try:
            return self.db.inserir_cliente(nome, cnh_numerica, telefone)
        except sqlite3.IntegrityError:
            raise ValueError("Já existe um cliente cadastrado com esta CNH.")

    def listar_clientes(self) -> list[dict]:
        return self.db.listar_clientes()

    # --- REGRAS DE AGENDAMENTOS ---
    def agendar_test_drive(self, veiculo_id: int, cliente_id: int, data_agendamento: str) -> int:
        try:
            data_obj = date.fromisoformat(data_agendamento)
        except ValueError:
            raise ValueError("Formato de data inválido. Use AAAA-MM-DD.")

        if data_obj < date.today():
            raise ValueError("Não é possível agendar test-drive para uma data passada.")

        veiculo = self.db.buscar_veiculo_por_id(veiculo_id)
        if not veiculo:
            raise ValueError("Veículo selecionado não existe.")
        if veiculo["status"] != "Disponível":
            raise ValueError(f"Veículo indisponível para agendamento (Status atual: {veiculo['status']}).")

        return self.db.inserir_agendamento(veiculo_id, cliente_id, data_agendamento)

    def finalizar_agendamento(self, agendamento_id: int, novo_status: str) -> None:
        if novo_status not in ("Concluído", "Cancelado"):
            raise ValueError("O agendamento só pode ser finalizado como 'Concluído' ou 'Cancelado'.")
        self.db.atualizar_status_agendamento(agendamento_id, novo_status)

    def listar_agendamentos(self) -> list[dict]:
        return self.db.listar_agendamentos()

    def obter_kpis(self) -> dict:
        veiculos = self.db.listar_veiculos()
        agendamentos = self.db.listar_agendamentos()
        return {
            "total_frota": len(veiculos),
            "disponiveis": sum(1 for v in veiculos if v["status"] == "Disponível"),
            "agendados": sum(1 for v in veiculos if v["status"] == "Agendado"),
            "manutencao": sum(1 for v in veiculos if v["status"] == "Em Manutenção"),
            "total_agendamentos": len(agendamentos),
        }