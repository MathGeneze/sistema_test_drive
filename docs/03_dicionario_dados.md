# Projeto de Dados e Dicionário de Dados

## 1. Normalização (3ª Forma Normal - 3FN)
O modelo relacional foi estruturado até a **3ª Forma Normal**:
* **1FN:** Todos os atributos são atômicos (ex.: `modelo` e `versao` separados; `cnh` armazenada apenas com dígitos).
* **2FN:** Todas as tabelas possuem chave primária simples (`id` autoincremental), eliminando dependências parciais.
* **3FN:** Não há dependências transitivas; dados descritivos do veículo e do cliente residem exclusivamente em suas respectivas tabelas, sendo referenciados na tabela `agendamentos` apenas por chaves estrangeiras (`veiculo_id` e `cliente_id`).

---

## 2. Dicionário de Dados

### Tabela: `veiculos`
Armazena os automóveis pertencentes à frota de test-drive da concessionária.

| Campo | Tipo SQLite | Tamanho / Domínio | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | Autoincremento | Não | PK | Identificador único do veículo. |
| `modelo` | TEXT | Texto livre (ex: Creta) | Não | - | Nome comercial do modelo do veículo. |
| `versao` | TEXT | Texto livre (ex: Ultimate) | Não | - | Pacote de acabamento e motorização. |
| `ano` | INTEGER | 2015 a 2030 | Não | - | Ano/modelo de fabricação do automóvel. |
| `placa` | TEXT | 7 caracteres (Unique) | Não | UK | Placa de identificação do veículo de frota. |
| `status` | TEXT | `Disponível`, `Agendado`, `Em Manutenção` | Não | - | Situação operacional atual do veículo. |

### Tabela: `clientes`
Armazena os dados dos clientes habilitados a realizar o test-drive.

| Campo | Tipo SQLite | Tamanho / Domínio | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | Autoincremento | Não | PK | Identificador único do cliente. |
| `nome` | TEXT | Texto livre | Não | - | Nome completo do condutor. |
| `cnh` | TEXT | 11 dígitos numéricos | Não | UK | Número de registro da CNH (sem pontuação). |
| `telefone` | TEXT | Texto formatado | Não | - | Telefone ou WhatsApp para contato. |

### Tabela: `agendamentos`
Registra as reservas de test-drive vinculando um cliente a um veículo.

| Campo | Tipo SQLite | Tamanho / Domínio | Nulo? | Chave | Descrição |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | Autoincremento | Não | PK | Identificador único do agendamento. |
| `veiculo_id` | INTEGER | Referência a `veiculos.id` | Não | FK | Identificador do veículo reservado. |
| `cliente_id` | INTEGER | Referência a `clientes.id` | Não | FK | Identificador do cliente condutor. |
| `data_agendamento`| TEXT | ISO-8601 (`YYYY-MM-DD`) | Não | - | Data agendada para realização do teste. |
| `status` | TEXT | `Confirmado`, `Concluído`, `Cancelado` | Não | - | Estado atual do ciclo de vida da reserva. |