from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from controllers.testdrive_controller import TestDriveController


def _aplicar_estilo_customizado() -> None:
    st.markdown(
        """
        <style>
        .main-header {
            padding: 1rem 1.25rem;
            border-radius: 10px;
            background: linear-gradient(90deg, #002C5F 0%, #00509E 100%);
            color: white;
            margin-bottom: 1.2rem;
        }
        .main-header h1 {
            margin: 0;
            font-size: 1.65rem;
        }
        .main-header p {
            margin: 0.25rem 0 0 0;
            font-size: 0.95rem;
            opacity: 0.9;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def renderizar_aplicacao(controller: TestDriveController) -> None:
    _aplicar_estilo_customizado()

    st.markdown(
        """
        <div class="main-header">
            <h1>🚗 Sistema de Gestão de Frota & Agendamento de Test-Drives</h1>
            <p>Controle operacional de veículos de demonstração, triagem de CNH e reservas de clientes</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    aba_frota, aba_clientes, aba_agendamentos = st.tabs(
        ["📊 Painel & Frota", "👤 Clientes", "📅 Agendamentos"]
    )

    # =========================================================================
    # ABA 1: PAINEL & FROTA
    # =========================================================================
    with aba_frota:
        kpis = controller.obter_kpis()
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total na Frota", kpis["total_frota"])
        col2.metric("Disponíveis", kpis["disponiveis"])
        col3.metric("Agendados", kpis["agendados"])
        col4.metric("Em Manutenção", kpis["manutencao"])
        col5.metric("Histórico Test-Drives", kpis["total_agendamentos"])

        st.divider()

        veiculos = controller.listar_veiculos()
        col_tabela, col_grafico = st.columns([1.6, 1])

        with col_tabela:
            st.subheader("Veículos da Frota de Demonstração")
            if veiculos:
                df_veiculos = pd.DataFrame(veiculos)
                df_veiculos.columns = ["ID", "Modelo", "Versão", "Ano", "Placa", "Status"]
                st.dataframe(df_veiculos, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum veículo cadastrado na frota.")

        with col_grafico:
            st.subheader("Distribuição por Status")
            if veiculos:
                df_status = pd.DataFrame(veiculos)["status"].value_counts().reset_index()
                df_status.columns = ["Status", "Quantidade"]
                cores = {
                    "Disponível": "#10B981",
                    "Agendado": "#3B82F6",
                    "Em Manutenção": "#F59E0B",
                }
                fig = px.pie(
                    df_status,
                    names="Status",
                    values="Quantidade",
                    hole=0.45,
                    color="Status",
                    color_discrete_map=cores,
                )
                fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260)
                st.plotly_chart(fig, use_container_width=True)

        st.divider()
        col_cad, col_status = st.columns(2)

        with col_cad:
            st.subheader("Cadastrar Novo Veículo")
            with st.form("form_veiculo", clear_on_submit=True):
                modelo = st.text_input("Modelo *", placeholder="Ex: Creta, HB20, Tucson")
                versao = st.text_input("Versão *", placeholder="Ex: Ultimate 1.6 TGDI")
                c_ano, c_placa = st.columns(2)
                ano = c_ano.number_input("Ano *", min_value=2015, max_value=2030, value=2026, step=1)
                placa = c_placa.text_input("Placa *", max_chars=7, placeholder="Ex: HYU2A26")
                submitted_v = st.form_submit_button("Adicionar à Frota", use_container_width=True)

                if submitted_v:
                    try:
                        controller.cadastrar_veiculo(modelo, versao, int(ano), placa)
                        st.success(f"Veículo {modelo} ({placa.upper()}) cadastrado com sucesso!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))

        with col_status:
            st.subheader("Alterar Status Operacional")
            if veiculos:
                with st.form("form_status_veiculo"):
                    opcoes_v = {
                        f"#{v['id']} - {v['modelo']} {v['versao']} ({v['placa']}) [{v['status']}]": v["id"]
                        for v in veiculos
                    }
                    veiculo_sel = st.selectbox("Selecione o Veículo", list(opcoes_v.keys()))
                    novo_status_v = st.selectbox(
                        "Novo Status", ["Disponível", "Em Manutenção", "Agendado"]
                    )
                    submitted_st = st.form_submit_button("Atualizar Status", use_container_width=True)

                    if submitted_st:
                        try:
                            controller.alterar_status_veiculo(opcoes_v[veiculo_sel], novo_status_v)
                            st.success("Status do veículo atualizado com sucesso!")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
            else:
                st.info("Cadastre um veículo para gerenciar status.")

    # =========================================================================
    # ABA 2: CLIENTES
    # =========================================================================
    with aba_clientes:
        col_form_c, col_lista_c = st.columns([1, 1.5])

        with col_form_c:
            st.subheader("Cadastrar Novo Cliente")
            with st.form("form_cliente", clear_on_submit=True):
                nome = st.text_input("Nome Completo *", placeholder="Ex: João da Silva")
                cnh = st.text_input("CNH (11 dígitos) *", max_chars=14, placeholder="Ex: 12345678901")
                telefone = st.text_input("Telefone / WhatsApp *", placeholder="Ex: (11) 99999-8888")
                submitted_c = st.form_submit_button("Salvar Cliente", use_container_width=True)

                if submitted_c:
                    try:
                        controller.cadastrar_cliente(nome, cnh, telefone)
                        st.success(f"Cliente {nome} cadastrado com sucesso!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))

        with col_lista_c:
            st.subheader("Clientes Habilitados Cadastrados")
            clientes = controller.listar_clientes()
            if clientes:
                df_clientes = pd.DataFrame(clientes)
                df_clientes.columns = ["ID", "Nome", "CNH", "Telefone"]
                st.dataframe(df_clientes, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum cliente cadastrado ainda.")

    # =========================================================================
    # ABA 3: AGENDAMENTOS
    # =========================================================================
    with aba_agendamentos:
        veiculos = controller.listar_veiculos()
        clientes = controller.listar_clientes()
        agendamentos = controller.listar_agendamentos()

        col_novo_ag, col_ger_ag = st.columns([1.2, 1])

        with col_novo_ag:
            st.subheader("Novo Agendamento de Test-Drive")
            if veiculos and clientes:
                with st.form("form_agendamento", clear_on_submit=True):
                    opcoes_veiculos = {
                        f"{v['modelo']} {v['versao']} ({v['placa']}) — [{v['status']}]": v["id"]
                        for v in veiculos
                    }
                    opcoes_clientes = {
                        f"{c['nome']} (CNH: {c['cnh']})": c["id"] for c in clientes
                    }

                    v_escolhido = st.selectbox("Veículo da Frota *", list(opcoes_veiculos.keys()))
                    c_escolhido = st.selectbox("Cliente Condutor *", list(opcoes_clientes.keys()))
                    data_ag = st.date_input("Data do Test-Drive *", value=date.today())

                    submitted_ag = st.form_submit_button("Confirmar Agendamento", use_container_width=True)

                    if submitted_ag:
                        try:
                            controller.agendar_test_drive(
                                opcoes_veiculos[v_escolhido],
                                opcoes_clientes[c_escolhido],
                                data_ag.isoformat(),
                            )
                            st.success("Test-drive agendado! O veículo foi reservado automaticamente.")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
            else:
                st.warning("É necessário ter ao menos um veículo e um cliente cadastrados.")

        with col_ger_ag:
            st.subheader("Encerrar ou Cancelar Reserva")
            ativos = [a for a in agendamentos if a["status"] == "Confirmado"]
            if ativos:
                with st.form("form_finalizar_ag"):
                    opcoes_ativos = {
                        f"#{a['id']} | {a['veiculo']} ({a['placa']}) — {a['cliente']} [{a['data_agendamento']}]": a["id"]
                        for a in ativos
                    }
                    ag_sel = st.selectbox("Agendamento Ativo", list(opcoes_ativos.keys()))
                    acao_ag = st.radio(
                        "Ação", ["Concluído", "Cancelado"], horizontal=True
                    )
                    submitted_fin = st.form_submit_button("Registrar Encerramento", use_container_width=True)

                    if submitted_fin:
                        try:
                            controller.finalizar_agendamento(opcoes_ativos[ag_sel], acao_ag)
                            st.success(f"Agendamento marcado como '{acao_ag}' e veículo liberado!")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))
            else:
                st.info("Não há agendamentos ativos pendentes de encerramento.")

        st.divider()
        st.subheader("Histórico Completo de Agendamentos")
        if agendamentos:
            df_ag = pd.DataFrame(agendamentos)
            df_ag = df_ag[["id", "veiculo", "placa", "cliente", "cnh", "data_agendamento", "status"]]
            df_ag.columns = ["ID", "Veículo", "Placa", "Cliente", "CNH", "Data", "Status"]
            st.dataframe(df_ag, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum agendamento registrado até o momento.")