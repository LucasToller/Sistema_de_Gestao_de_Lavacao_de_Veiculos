-- POPULANDO TABELA ENDERECO
INSERT INTO endereco (logradouro, numero, complemento, bairro, cidade, cep) VALUES
('Rua A', '123', 'Próximo à praça', 'Centro', 'Balneário Piçarras', '88380-000'),
('Rua B', '456', 'Casa azul', 'Praia', 'Penha', '88385-000'),
('Rua C', '789', NULL, 'Fazenda', 'Itajaí', '88301-000');


-- POPULANDO TABELA CLIENTE
INSERT INTO cliente (nome, cpf, email, data_cadastro, status, id_endereco) VALUES
('João Silva', '111.111.111-11', 'joao.silva@example.com', '2025-11-30', 'ATIVO', 1),
('Maria Oliveira','222.222.222-22', 'maria.oliveira@example.com','2025-11-28', 'ATIVO', 2),
('Carlos Souza',  '333.333.333-33', 'carlos.souza@example.com', '2025-11-25', 'ATIVO', 3);


-- POPULANDO TABELA TELEFONE_CLIENTE
INSERT INTO telefone_cliente (numero, id_cliente) VALUES
('(47) 99999-0001', 1),
('(47) 98888-0002', 2),
('(47) 97777-0003', 3);


-- POPULANDO TABELA FUNCIONARIO
INSERT INTO funcionario (nome, cpf, data_contratacao, cargo, salario, email, status, id_endereco) VALUES
('Lucas T.', '444.444.444-44', '2024-01-10', 'Atendente', 2200.00, 'lucas@example.com',   'ATIVO', 1),
('Victor M.', '555.555.555-55', '2023-08-15', 'Auxiliar',  2000.00, 'eduardo@example.com', 'ATIVO', 2);


-- POPULANDO TABELA TELEFONE_FUNCIONARIO
INSERT INTO telefone_funcionario (numero, id_funcionario) VALUES
('(47) 96666-0001', 1),
('(47) 97777-0002', 2);


-- POPULANDO TABELA VEICULO
INSERT INTO veiculo (marca, modelo, ano, cor, placa, tipo, id_cliente) VALUES
('Chevrolet', 'Onix', 2020, 'Prata', 'ABC1D23', 'Carro', 1),
('Hyundai', 'HB20', 2019, 'Branco', 'XYZ4E56', 'Carro', 1),
('Volkswagen', 'Gol', 2015, 'Preto', 'QWE9R87', 'Carro', 2),
('Honda', 'CG 160', 2022, 'Vermelho', 'MNO3P21', 'Moto', 3);


-- POPULANDO TABELA SERVICO
INSERT INTO servico (nome, descricao, duracao_estimada_min, valor_base, ativo) VALUES
('Lavagem Simples', 'Lavagem externa com secagem', 30,  30.00, 'S'),
('Lavagem Completa', 'Lavagem externa e interna com secagem', 60,  50.00, 'S'),
('Higienização', 'Limpeza interna detalhada, bancos e carpetes', 90, 120.00, 'S'),
('Polimento', 'Polimento da pintura com proteção', 120, 200.00, 'S');

-- POPULANDO TABELA FORMA_PAGAMENTO
INSERT INTO forma_pagamento (descricao, permite_parcelamento, ativo) VALUES
('DINHEIRO', 'N', 'S'),
('PIX','N', 'S'),
('CARTAO_DEBITO', 'N', 'S'),
('CARTAO_CREDITO', 'S', 'S');


-- POPULANDO TABELA ORDEM_SERVICO
INSERT INTO ordem_servico (
    data_hora_entrada, data_hora_saida, status, observacoes,
    valor_total_previsto, valor_total_final, id_cliente, id_veiculo, id_funcionario
) VALUES
('2025-11-30 09:15:00', '2025-11-30 10:00:00', 'CONCLUIDA',
 'Carro muito empoeirado', 50.00, 50.00, 1, 1, 1),
('2025-11-30 10:30:00', NULL, 'EM_EXECUCAO',
 'Cliente pediu capricho na parte interna', 170.00, NULL, 2, 3, 2),
('2025-11-30 11:00:00', NULL, 'ABERTA',
 'Primeira vez do cliente na lavação', 30.00, NULL, 3, 4, 1);


-- POPULANDO TABELA ITEM_OS:

-- OS 1 (João, Onix) - Lavagem Completa
INSERT INTO item_os (
    quantidade, valor_unitario, valor_total_item, id_ordem_servico, id_servico
) VALUES
(1, 50.00, 50.00, 1, 2);

-- OS 2 (Maria, Gol) - Lavagem Completa + Higienização
INSERT INTO item_os (
    quantidade, valor_unitario, valor_total_item, id_ordem_servico, id_servico
) VALUES
(1, 50.00,  50.00, 2, 2),
(1, 120.00, 120.00, 2, 3);

-- OS 3 (Carlos, Moto) - Lavagem Simples
INSERT INTO item_os (
    quantidade, valor_unitario, valor_total_item, id_ordem_servico, id_servico
) VALUES
(1, 30.00, 30.00, 3, 1);


-- POPULANDO TABELA PAGAMENTO:

-- OS 1 paga em dinheiro
INSERT INTO pagamento (
    data_pagamento, valor_pagamento, status, observacoes, id_ordem_servico, id_forma_pagamento
) VALUES
('2025-11-30 10:05:00', 50.00, 'EFETIVADO', 'Pagamento em dinheiro', 1, 1);

-- OS 2 paga parte em pix, parte no crédito
INSERT INTO pagamento (
    data_pagamento, valor_pagamento, status, observacoes, id_ordem_servico, id_forma_pagamento
) VALUES
('2025-11-30 11:30:00', 100.00, 'EFETIVADO', 'Entrada via PIX', 2, 2),
('2025-11-30 11:31:00',  70.00, 'PENDENTE', 'Restante no crédito', 2, 4);