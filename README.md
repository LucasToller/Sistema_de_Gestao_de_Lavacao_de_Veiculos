# Sistema de Gestão de Lavação de Veículos

Projeto desenvolvido para a **Atividade Avaliativa M3 – Projeto/Desenvolvimento**  
da disciplina de **Banco de Dados I – UNIVALI (Escola Politécnica)**.

O objetivo foi modelar e implementar um sistema de gestão para uma lavação de veículos,
com foco na qualidade da modelagem do banco de dados relacional e na implementação
de CRUDs básicos em Python com persistência no MySQL.

---

## 🧱 Funcionalidades principais

- Cadastro de **clientes** e seus endereços/telefones
- Cadastro de **veículos** vinculados aos clientes
- Abertura e manutenção de **ordens de serviço (OS)**
- Registro dos **serviços** realizados em cada OS (itens da OS)
- Registro de **pagamentos** e formas de pagamento
- Interface em **linha de comando**, com menu interativo

---

## 🛠️ Tecnologias utilizadas

- **MySQL 8.x**
- **MySQL Workbench**
- **Python 3.x**
- Biblioteca **mysql-connector-python** para conexão com o banco de dados

---

## 📁 Estrutura do repositório

/
├── Banco de Dados SQL/
│   ├── 01_criacao_schema_lava_car.sql   # Criação do banco e das tabelas
│   └── 02_populamento_lava_car.sql      # Inserts de dados de exemplo
│
├── Scripts Python/
│   ├── main.py                          # Menu principal da aplicação
│   ├── db_config.py                     # Configuração de conexão com MySQL
│   ├── utils.py                         # Funções auxiliares (validação de input, etc.)
│   ├── crud_clientes.py                 # CRUD de clientes
│   ├── crud_veiculos.py                 # CRUD de veículos
│   └── crud_ordens_servico.py           # CRUD de ordens de serviço
│
└── README.md                            # Este arquivo


---

## ▶️ Como executar o projeto

1. **Clonar o repositório**

   ```bash
   git clone https://github.com/SEU_USUARIO/Sistema_de_Gestao_de_Lavacao_de_Veiculos.git
   cd Sistema_de_Gestao_de_Lavacao_de_Veiculos
   ```

2. **Criar o banco de dados**

   * Abrir o **MySQL Workbench**.
   * Executar o script `01_criacao_schema_lava_car.sql` (pasta *Banco de Dados SQL*).
   * Em seguida, executar `02_populamento_lava_car.sql` para inserir os dados de exemplo.

3. **Configurar a conexão no Python**

   * Editar o arquivo `db_config.py` (pasta *Scripts Python*) ajustando:

     * `host`
     * `user`
     * `password`
     * `database` (deve ser `lava_car`)

4. **Instalar dependências Python**

   ```bash
   pip install mysql-connector-python
   ```

5. **Executar a aplicação**

   ```bash
   cd "Scripts Python"
   python main.py
   ```

   O sistema abrirá um menu no terminal, permitindo acessar os CRUDs de:

   * Clientes
   * Veículos
   * Ordens de serviço

---

## 👨‍💻 Autores

* Lucas Toller Gutmann
* Victor Matheus da Silva Moreira 

---

## 📌 Observações

Este projeto foi desenvolvido com fins acadêmicos, para demonstrar:

* Modelagem conceitual (DER), lógica e física de banco de dados
* Normalização básica das tabelas
* Uso de chaves primárias e estrangeiras
* Integração de uma aplicação Python com um banco de dados MySQL utilizando comandos SQL explícitos.
