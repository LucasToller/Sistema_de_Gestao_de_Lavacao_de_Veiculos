-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS lava_car
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE lava_car;

-- TABELA ENDERECO
CREATE TABLE endereco (
    id INT AUTO_INCREMENT PRIMARY KEY,
    logradouro VARCHAR(100) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(100),
    bairro VARCHAR(60) NOT NULL,
    cidade VARCHAR(60) NOT NULL,
    cep VARCHAR(9) NOT NULL
) ENGINE=InnoDB;

-- TABELA CLIENTE
CREATE TABLE cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14),
    email VARCHAR(100),
    data_cadastro DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    id_endereco INT NOT NULL,
    CONSTRAINT fk_cliente_endereco
        FOREIGN KEY (id_endereco)
        REFERENCES endereco(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABELA TELEFONE_CLIENTE
CREATE TABLE telefone_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    id_cliente INT NOT NULL,
    CONSTRAINT fk_tel_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- TABELA FUNCIONARIO
CREATE TABLE funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14),
    data_contratacao DATE NOT NULL,
    cargo VARCHAR(60) NOT NULL,
    salario DECIMAL(10,2),
    email VARCHAR(100),
    status VARCHAR(20) NOT NULL,
    id_endereco INT NOT NULL,
    CONSTRAINT fk_func_endereco
        FOREIGN KEY (id_endereco)
        REFERENCES endereco(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABELA TELEFONE_FUNCIONARIO
CREATE TABLE telefone_funcionario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL,
    id_funcionario INT NOT NULL,
    CONSTRAINT fk_tel_funcionario
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionario(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- TABELA VEICULO
CREATE TABLE veiculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(60),
    modelo VARCHAR(60) NOT NULL,
    ano INT,
    cor VARCHAR(30),
    placa VARCHAR(10) NOT NULL,
    tipo VARCHAR(30),
    id_cliente INT NOT NULL,
    CONSTRAINT fk_veiculo_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABELA SERVICO
CREATE TABLE servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(80) NOT NULL,
    descricao VARCHAR(255),
    duracao_estimada_min INT,
    valor_base DECIMAL(10,2) NOT NULL,
    ativo CHAR(1) DEFAULT 'S'
) ENGINE=InnoDB;

-- TABELA ORDEM_SERVICO
CREATE TABLE ordem_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora_entrada DATETIME NOT NULL,
    data_hora_saida DATETIME,
    status VARCHAR(20) NOT NULL,
    observacoes VARCHAR(255),
    valor_total_previsto DECIMAL(10,2),
    valor_total_final DECIMAL(10,2),
    id_cliente INT NOT NULL,
    id_veiculo INT NOT NULL,
    id_funcionario INT NOT NULL,
    CONSTRAINT fk_os_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_os_veiculo
        FOREIGN KEY (id_veiculo)
        REFERENCES veiculo(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_os_funcionario
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionario(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABELA ITEM_OS
CREATE TABLE item_os (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quantidade INT NOT NULL,
    valor_unitario DECIMAL(10,2) NOT NULL,
    valor_total_item DECIMAL(10,2) NOT NULL,
    id_ordem_servico INT NOT NULL,
    id_servico INT NOT NULL,
    CONSTRAINT fk_item_os
        FOREIGN KEY (id_ordem_servico)
        REFERENCES ordem_servico(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_item_servico
        FOREIGN KEY (id_servico)
        REFERENCES servico(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- TABELA FORMA_PAGAMENTO
CREATE TABLE forma_pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL,
    permite_parcelamento CHAR(1) DEFAULT 'N',
    ativo CHAR(1) DEFAULT 'S'
) ENGINE=InnoDB;

-- TABELA PAGAMENTO
CREATE TABLE pagamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_pagamento DATETIME NOT NULL,
    valor_pagamento DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    observacoes VARCHAR(255),
    id_ordem_servico INT NOT NULL,
    id_forma_pagamento INT NOT NULL,
    CONSTRAINT fk_pagamento_os
        FOREIGN KEY (id_ordem_servico)
        REFERENCES ordem_servico(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_pagamento_forma
        FOREIGN KEY (id_forma_pagamento)
        REFERENCES forma_pagamento(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;