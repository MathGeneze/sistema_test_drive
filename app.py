import streamlit as st
from models.database import DatabaseModel
from models.seed import popular_dados_iniciais
from controllers.testdrive_controller import TestDriveController
from views.dashboard_view import renderizar_aplicacao


def main() -> None:
    st.set_page_config(
        page_title="Gestão de Test-Drive | Frota",
        page_icon="🚗",
        layout="wide",
    )

    db = DatabaseModel()
    popular_dados_iniciais(db)
    controller = TestDriveController(db=db)

    renderizar_aplicacao(controller)


if __name__ == "__main__":
    main()