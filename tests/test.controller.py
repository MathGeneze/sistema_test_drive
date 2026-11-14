from datetime import date, timedelta
import pytest
from models.database import DatabaseModel
from controllers.testdrive_controller import TestDriveController


@pytest.fixture
def controller(tmp_path):
    db_teste = DatabaseModel(db_path=tmp_path / "teste_unitario.db")
    return TestDriveController(db=db_teste)


def test_cadastrar_cliente_valido(controller):
    cliente_id = controller.cadastrar_cliente("Carlos Silva", "123.456.789-01", "11999998888")
    assert cliente_id == 1
    clientes = controller.listar_clientes()
    assert clientes[0]["cnh"] == "12345678901"


def test_bloquear_cnh_invalida(controller):
    with pytest.raises(ValueError, match="11 dígitos"):
        controller.cadastrar_cliente("Ana Souza", "12345", "11988887777")


def test_fluxo_completo_agendamento_e_conclusao(controller):
    v_id = controller.cadastrar_veiculo("Creta", "Ultimate", 2026, "ABC1D23")
    c_id = controller.cadastrar_cliente("Pedro Santos", "98765432100", "11977776666")
    amanha = (date.today() + timedelta(days=1)).isoformat()

    ag_id = controller.agendar_test_drive(v_id, c_id, amanha)
    assert ag_id == 1

    # Veículo deve mudar automaticamente para 'Agendado'
    veiculo = controller.listar_veiculos()[0]
    assert veiculo["status"] == "Agendado"

    # Concluir o test-drive deve liberar o veículo novamente
    controller.finalizar_agendamento(ag_id, "Concluído")
    veiculo_liberado = controller.listar_veiculos()[0]
    assert veiculo_liberado["status"] == "Disponível"


def test_bloquear_agendamento_veiculo_indisponivel(controller):
    v_id = controller.cadastrar_veiculo("HB20", "Platinum", 2026, "XYZ9K88")
    controller.alterar_status_veiculo(v_id, "Em Manutenção")
    c_id = controller.cadastrar_cliente("Julia Lima", "11122233344", "11966665555")
    amanha = (date.today() + timedelta(days=1)).isoformat()

    with pytest.raises(ValueError, match="indisponível"):
        controller.agendar_test_drive(v_id, c_id, amanha)


def test_bloquear_agendamento_data_passada(controller):
    v_id = controller.cadastrar_veiculo("Tucson", "Limited", 2025, "HYU5F55")
    c_id = controller.cadastrar_cliente("Roberto Dias", "55566677788", "11955554444")
    ontem = (date.today() - timedelta(days=1)).isoformat()

    with pytest.raises(ValueError, match="data passada"):
        controller.agendar_test_drive(v_id, c_id, ontem)