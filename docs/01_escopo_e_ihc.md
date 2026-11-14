# Escopo, Requisitos e Diretrizes de IHC

## 1. Visão Geral e Escopo do Projeto
O **Sistema de Gestão de Frota e Agendamento de Test-Drives** é uma aplicação web desenvolvida para otimizar a operação diária de concessionárias automotivas. O sistema centraliza o controle dos veículos destinados à frota de demonstração, realiza a triagem cadastral de clientes condutores e gerencia os agendamentos de test-drives, evitando conflitos de reserva e garantindo que apenas veículos aptos e clientes com CNH válida sejam liberados.

## 2. Requisitos Funcionais (RF)
* **RF01 – Gestão da Frota:** Permitir o cadastro, consulta e atualização de status de veículos de demonstração (`Disponível`, `Agendado`, `Em Manutenção`).
* **RF02 – Cadastro de Clientes:** Permitir o registro e listagem de clientes interessados, exigindo nome completo, telefone e CNH válida (11 dígitos numéricos únicos).
* **RF03 – Agendamento de Test-Drive:** Vincular um cliente cadastrado a um veículo com status `Disponível` em uma data válida (igual ou posterior à data atual).
* **RF04 – Controle Automático de Disponibilidade:** Alterar automaticamente o status do veículo para `Agendado` ao confirmar uma reserva e retorná-lo para `Disponível` quando o agendamento for marcado como `Concluído` ou `Cancelado`.
* **RF05 – Painel Gerencial (KPIs):** Exibir indicadores em tempo real com o total de veículos na frota, quantidade disponível para teste e histórico de agendamentos.

## 3. Requisitos Não Funcionais (RNF)
* **RNF01 – Arquitetura:** Aplicação estruturada no padrão MVC (*Model-View-Controller*) em Python, garantindo separação entre regras de negócio, persistência e interface.
* **RNF02 – Persistência:** Banco de dados relacional SQLite, leve, portável e de fácil manutenção.
* **RNF03 – Usabilidade e IHC:** Interface web responsiva construída em Streamlit, com navegação por abas e feedback visual imediato.
* **RNF04 – Confiabilidade:** Validação de regras de negócio coberta por testes unitários automatizados via Pytest.

## 4. Diretrizes de Interface Humano-Computador (IHC)
Com base nas boas práticas de usabilidade, a interface foi projetada seguindo quatro pilares:
1. **Clareza e Consistência:** Organização em três abas principais (*Painel & Frota*, *Clientes* e *Agendamentos*) com padrões uniformes de formulários e tabelas.
2. **Feedback Imediato:** Uso de mensagens visuais explícitas (`st.success` para operações concluídas e `st.error` para bloqueios de regra de negócio, como CNH inválida ou carro indisponível).
3. **Prevenção de Erros:** Campos de seleção (`selectbox`) filtrados para exibir preferencialmente veículos disponíveis e seletores de data que orientam o preenchimento correto.
4. **Reversibilidade:** Possibilidade de cancelar um agendamento ativo ou alterar o status de manutenção de um veículo a qualquer momento.