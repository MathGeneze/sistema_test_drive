# 🚗 Sistema de Gestão de Frota e Agendamento de Test-Drives

Projeto desenvolvido para a disciplina **Projeto Integrador Transdisciplinar em Engenharia de Software II** (Cruzeiro do Sul Virtual).

## 🎯 Objetivo
Centralizar o controle da frota de demonstração de uma concessionária automotiva, realizando a triagem cadastral de condutores (validação de CNH) e o agendamento de test-drives com bloqueio automático de veículos reservados ou em manutenção.

## 🏗️ Arquitetura (Padrão MVC)
O projeto segue a separação de responsabilidades no padrão **Model-View-Controller**:
* `models/` — Conexão com banco relacional **SQLite**, script DDL (`schema.sql`) e carga inicial (`seed.py`).
* `controllers/` — Regras de negócio, validações de CNH, datas e controle de disponibilidade da frota.
* `views/` e `app.py` — Interface web interativa desenvolvida em **Streamlit** com indicadores e gráficos em **Plotly**.
* `tests/` — Suíte de testes unitários automatizados com **Pytest**.
* `docs/` — Documentação acadêmica (Escopo, IHC, Diagramas UML em Mermaid e Dicionário de Dados).

## 🚀 Como Executar Localmente
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt