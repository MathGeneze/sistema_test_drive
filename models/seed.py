from models.database import DatabaseModel


def popular_dados_iniciais(db: DatabaseModel) -> None:
    if db.listar_veiculos():
        return  # Evita duplicar dados se o banco já estiver populado

    veiculos_iniciais = [
        ("HB20", "Platinum Safety 1.0 TGDI", 2026, "HYU2A26", "Disponível"),
        ("Creta", "Ultimate 1.6 TGDI", 2026, "CRE9B26", "Disponível"),
        ("Tucson", "Limited 1.6 Turbo", 2025, "TUC4C25", "Disponível"),
        ("Kona", "Hybrid Signature", 2026, "KON7D26", "Em Manutenção"),
        ("Ioniq 5", "Signature AWD Elétrico", 2026, "ION1E26", "Disponível"),
    ]
    for modelo, versao, ano, placa, status in veiculos_iniciais:
        db.inserir_veiculo(modelo, versao, ano, placa, status)

    clientes_iniciais = [
        ("Lucas Almeida", "12345678901", "(11) 98765-4321"),
        ("Mariana Costa", "98765432100", "(11) 91234-5678"),
    ]
    for nome, cnh, telefone in clientes_iniciais:
        db.inserir_cliente(nome, cnh, telefone)