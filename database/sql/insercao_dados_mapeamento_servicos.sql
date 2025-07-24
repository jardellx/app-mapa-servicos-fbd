-- Inserções na tabela Usuario
INSERT INTO Usuario VALUES
(1, 'Leandro Davi', 'ldavi0561@gmail.com', 'senha1', '2006-03-16'),
(2, 'Francisco Jardel', 'jardelmagalhaes12@gmail.com', 'senha2', '2001-06-27'),
(3, 'Jardeson Magalhaes', 'jardesonofc@gmail.com', 'senha3', '2002-07-06'),
(4, 'Liz Mota', 'lizmsf@gmail.com', 'senha4', '2009-06-07'),
(5, 'Luis Miguel', 'lmiguellr11@gmail.com', 'senha5', '2010-10-07'),
(6, 'Kaylane Maria', 'kaymf0@gmail.com', 'senha6', '2005-10-27'),
(7, 'Ana Marcia', 'macinhacruz@hotmail.com.br', 'senha7', '1974-08-27'),
(8, 'Maria Fernanda', 'mafernanda@gmail.com', 'senha8', '2004-03-31'),
(9, 'Ricardo Silveira', 'prefeito@yahoo.com.br', 'senha9', '1975-03-19'),
(10, 'Cristiano Ronaldo', 'cr7@gmail.com', 'senha10', '1985-02-05');

-- Inserções na tabela Usuario_comum
INSERT INTO Usuario_comum VALUES
(1, '-4.971597, -39.021746'),
(2, '-4.970593, -39.017840'),
(3, '-4.968674, -39.011167'),
(4, '-4.958840, -39.030737'),
(5, '-4.967562, -39.002670'),
(6, '-4.978865, -39.056544'),
(7, '-4.965370, -39.017749'),
(8, '-4.970244, -39.007277'),
(9, '-4.971527, -39.026640'),
(10, '-4.969817, -39.014487');

-- Inserções na tabela Adm
INSERT INTO Adm VALUES
(1, 1),
(2, 1),
(3, 2),
(8, 3);

-- Inserções na tabela Servico
INSERT INTO Servico VALUES
(1, 'CRAS CAMPO NOVO', '07:30-17:30', 'Assistencia Social', 'AVENIDA PRESIDENTE VARGAS', 'QUIXADA', NULL, 'CAMPO NOVO'),
(2, 'CAPS DE QUIXADA 2', '07:30-17:30', 'Saude', 'RUA BRASILIO EMILIANO PINTO', 'QUIXADA', NULL, 'COMBATE'),
(3, 'CAPS INFANTIL DE QUIXADA', '07:30-17:30', 'Saude', 'RUA DR RUI MAIA', 'QUIXADA', NULL, 'CENTRO'),
(4, 'CEO DE QUIXADÁ CENTRO DE ESPECIALIDADES', '07:30-17:30', 'Saude', 'RUA JOSÉ ENEAS MONTEIRO LESSA', 'QUIXADA', NULL, 'PLANALTO UNIVERSITARIO'),
(5, 'UPA 24H DE QUIXADA', '00:00-23:59', 'Saude', 'RUA DOS VOLUNTARIOS', 'QUIXADA', NULL, 'PLANALTO RENASCER'),
(6, 'SERVIÇO DE ATENÇÃO DOMICILIAR SAD DE QUIXADA', '07:30-17:30', 'Saude', 'RUA FRANCISCO ENEAS DE LIMA', 'QUIXADA', NULL, 'CENTRO'),
(7, 'CENTRO DE EDUCAÇÃO INFANTIL MONSENHOR LUIZ ORLANDO DE LIMA', '07:00-17:00', 'Educacao', 'RUA NOVO AMANHECER', 'QUIXADA', NULL, 'RENASCER'),
(8, 'ESCOLA DE ENSINO FUNDAMENTAL RACHEL DE QUEIROZ', '07:00-17:00', 'Educacao', 'RUA GERALDO BEZERRA QUEIROZ', 'QUIXADA', NULL, 'RESIDENCIAL RACHEL DE QUEIROZ'),
(9, 'ESCOLA DE ENSINO FUNDAMENTAL DEP. FLÁVIO PORTELA MARCILIO', '07:30-17:00', 'Educacao', 'RUA JOSÉ DE QUEIROZ PESSOA', 'QUIXADA', NULL, 'CENTRO'),
(10, 'ESCOLA DE ENSINO FUNDAMENTAL ROSA BAQUIT', '07:00-17:00', 'Educacao', 'RUA ABRÃO BAQUIT', 'QUIXADA', NULL, 'CARRASCAL');

-- Inserções na tabela telefone_servico
INSERT INTO telefone_servico VALUES
(1, '(88) 9813-9800'),
(2, '(88) 9.9202-4217'),
(3, '(88) 9.9202-42176'),
(4, '(88) 9.9202-4217'),
(5, '(88) 9.9202-4217'),
(6, '(88) 9.9202-4217'),
(7, '(88) 9.9202-4217'),
(8, '(88) 9.9202-4217'),
(9, '(88) 9.9202-4217'),
(10, '(88) 9.9202-4217');

-- Inserções na tabela Avaliacao
INSERT INTO Avaliacao VALUES
(9, 4, '2025-05-30', 5, 'Muito bom.'),
(7, 2, '2025-02-18', 4, 'Fui muito bem atendido.'),
(10, 5, '2025-04-10', 3, 'Atendimento um tanto demorado.'),
(3, 10, '2025-05-05', 5, NULL),
(5, 1, '2025-01-31', 5, 'Excelente!'),
(6, 3, '2025-01-18', 4, NULL),
(8, 9, '2025-05-16', 3, 'Precisa de reforma.'),
(4, 10, '2025-01-18', 4, NULL),
(1, 8, '2025-07-20', 2, NULL),
(2, 5, '2025-07-08', 1, NULL);

-- Inserções na tabela Historico_De_Pesquisas
INSERT INTO Historico_De_Pesquisas VALUES
(9, 5, '2025-05-18'),
(10, 6, '2025-07-13'),
(3, 4, '2025-05-21'),
(2, 1, '2025-04-02'),
(4, 5, '2025-03-13'),
(2, 4, '2025-02-20'),
(1, 7, '2025-01-01'),
(5, 8, '2025-06-28'),
(6, 3, '2025-07-17'),
(6, 6, '2025-02-19');

-- Inserções na tabela Favorita
INSERT INTO Favorita VALUES
(4, 5),
(2, 10),
(3, 9),
(4, 3),
(8, 7),
(5, 9),
(4, 6),
(1, 4),
(5, 6),
(7, 5);

-- Inserções na tabela Relatorio_Avaliacao
INSERT INTO Relatorio_Avaliacao VALUES
(1, 1, 2, '2025-03-06', '2025-02-01', '2025-02-19', 'Média de avaliações: 4.2.'),
(2, 2, 4, '2025-04-30', '2025-01-27', '2025-04-04', 'Total de avaliações: 20.'),
(3, 3, 7, '2025-06-12', '2025-06-05', '2025-06-08', 'Média de avaliações: 3.2.'),
(4, 1, 3, '2025-02-24', '2025-02-20', '2025-02-24', 'Média de avaliações: 2.9.'),
(5, 2, 5, '2025-05-22', '2025-05-18', '2025-05-22', 'Total de avaliações: 04.'),
(6, 3, 10, '2025-06-18', '2025-06-05', '2025-06-12', 'Média de avaliações: 4.7.'),
(7, 1, 9, '2025-02-10', '2025-02-01', '2025-02-10', 'Total de pesquisas: 18.'),
(8, 2, 8, '2025-04-09', '2025-04-01', '2025-04-05', 'Total de pesquisas: 05.'),
(9, 3, 6, '2025-01-15', '2025-01-01', '2025-01-14', 'Total de pesquisas: 18.'),
(10, 2, 1, '2025-07-10', '2025-06-01', '2025-06-30', 'Total de pesquisas: 42.');

-- Inserções na tabela adm_atualiza_servico
INSERT INTO adm_atualiza_servico VALUES
(1, 1),
(2, 2),
(3, 3),
(3, 4),
(2, 5),
(1, 6),
(1, 7),
(2, 8),
(3, 9),
(1, 10);
