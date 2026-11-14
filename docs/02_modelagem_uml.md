# Modelagem UML da Solução

## 1. Diagrama de Casos de Uso
Representa as interações dos atores da concessionária (Vendedor/Recepcionista e Gerente de Frota) com o sistema.

```mermaid
flowchart LR
    Vendedor(["👤 Vendedor / Recepção"])
    Gerente(["👤 Gerente de Frota"])

    subgraph Sistema ["Sistema de Gestão de Test-Drive"]
        UC1("Cadastrar e Consultar Clientes")
        UC2("Agendar Test-Drive")
        UC3("Concluir ou Cancelar Test-Drive")
        UC4("Cadastrar Veículo na Frota")
        UC5("Alterar Status de Manutenção")
        UC6("Visualizar Indicadores da Frota")
    end

    Vendedor --> UC1
    Vendedor --> UC2
    Vendedor --> UC3
    Vendedor --> UC6

    Gerente --> UC4
    Gerente --> UC5
    Gerente --> UC6