PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL,
    versao TEXT NOT NULL,
    ano INTEGER NOT NULL CHECK (ano >= 2015 AND ano <= 2030),
    placa TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'Disponível' 
        CHECK (status IN ('Disponível', 'Agendado', 'Em Manutenção'))
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnh TEXT NOT NULL UNIQUE CHECK (length(cnh) = 11),
    telefone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS agendamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    veiculo_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    data_agendamento TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Confirmado' 
        CHECK (status IN ('Confirmado', 'Concluído', 'Cancelado')),
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE RESTRICT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
);