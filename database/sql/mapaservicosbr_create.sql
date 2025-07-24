CREATE TABLE Usuario(
id_usuario SERIAL PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
email VARCHAR(100) NOT NULL UNIQUE,
senha VARCHAR(10) NOT NULL,
data_nascimento DATE NOT NULL
);

CREATE TABLE Usuario_comum(
id_usuario INT PRIMARY KEY,
loc_atual_coord VARCHAR(100),
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Adm(
id_usuario INT PRIMARY KEY,
nivel_acesso VARCHAR(100),
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE servico(
id_servico SERIAL PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
horario_funcionamento VARCHAR(100) NOT NULL,
Categoria VARCHAR(50) NOT NULL,
rua VARCHAR(100) NOT NULL,
cidade VARCHAR(100) NOT NULL,
numero VARCHAR(10),
bairro VARCHAR(100) NOT NULL
); -- <-- PONTO E VÍRGULA ADICIONADO AQUI!

CREATE TABLE telefone_servico (
id_servico INT,
numero_telefone VARCHAR(20) NOT NULL,
PRIMARY KEY (id_servico, numero_telefone),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Avaliacao (
id_usuario INT,
id_servico INT,
data_avaliacao DATE NOT NULL,
nota INT NOT NULL,
comentario TEXT,
PRIMARY KEY (id_usuario, id_servico),
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Historico_De_Pesquisas (
id_usuario INT NOT NULL,
id_servico INT NOT NULL,
data_pesq DATE NOT NULL,
PRIMARY KEY (id_usuario, id_servico, data_pesq),
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Favorita (
id_usuario INT,
id_servico INT,
PRIMARY KEY (id_usuario, id_servico),
FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Relatorio_Avaliacao (
id SERIAL PRIMARY KEY,
id_adm INT,
id_servico INT,
data_geracao DATE NOT NULL,
periodo_inicial DATE NOT NULL,
periodo_final DATE NOT NULL,
conteudo_relatorio TEXT NOT NULL,
FOREIGN KEY (id_adm) REFERENCES Adm(id_usuario),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);

CREATE TABLE Adm_Atualiza_Servico (
id_usuario INT,
id_servico INT,
PRIMARY KEY (id_usuario, id_servico),
FOREIGN KEY (id_usuario) REFERENCES Adm(id_usuario),
FOREIGN KEY (id_servico) REFERENCES Servico(id_servico)
);