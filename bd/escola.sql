-- DROPs --

DROP TABLE IF EXISTS Frequencias;
DROP TABLE IF EXISTS Notas;
DROP TABLE IF EXISTS Disciplinas;
DROP TABLE IF EXISTS Usuarios;
DROP TABLE IF EXISTS Atividades_Alunos;
DROP TABLE IF EXISTS Presencas;
DROP TABLE IF EXISTS Pagamentos;
DROP TABLE IF EXISTS Alunos;
DROP TABLE IF EXISTS Turmas;
DROP TABLE IF EXISTS Atividades;
DROP TABLE IF EXISTS Professores;


-- CREATE TABLES --

CREATE TABLE Professores (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE Atividades (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL
);

CREATE TABLE Turmas (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT REFERENCES Professores(id_professor),
    horario VARCHAR(100) NOT NULL
);

CREATE TABLE Alunos (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT REFERENCES Turmas(id_turma),
    nome_responsavel VARCHAR(255) NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    email_responsavel VARCHAR(100) NOT NULL,
    informacoes_adicionais TEXT
);

CREATE TABLE Pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Alunos(id_aluno),
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    referencia VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE Presencas (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Alunos(id_aluno),
    data_presenca DATE NOT NULL,
    presente BOOLEAN NOT NULL
);

CREATE TABLE Atividades_Alunos (
    id_atividade INT REFERENCES Atividades(id_atividade),
    id_aluno INT REFERENCES Alunos(id_aluno),
    PRIMARY KEY (id_atividade, id_aluno)
);

CREATE TABLE Usuarios (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20) NOT NULL,
    id_professor INT REFERENCES Professores(id_professor)
);

CREATE TABLE Disciplinas (
    id_disciplina SERIAL PRIMARY KEY,
    nome_disciplina VARCHAR(100) NOT NULL,
    id_professor INT REFERENCES Professores(id_professor)
);

CREATE TABLE Notas (
    id_nota SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Alunos(id_aluno),
    id_disciplina INT REFERENCES Disciplinas(id_disciplina),
    valor_nota DECIMAL(4,2) NOT NULL,
    data_avaliacao DATE NOT NULL
);

CREATE TABLE Frequencias (
    id_frequencia SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Alunos(id_aluno),
    id_disciplina INT REFERENCES Disciplinas(id_disciplina),
    data_aula DATE NOT NULL,
    presente BOOLEAN NOT NULL
);


-- INSERTS --

INSERT INTO Professores (nome_completo, email, telefone) VALUES
('Ana Paula Silva', 'ana.silva@escola.com', '11999990001'),
('Carlos Eduardo Souza', 'carlos.souza@escola.com', '11999990002'),
('Mariana Oliveira', 'mariana.oliveira@escola.com', '11999990003');

INSERT INTO Atividades (descricao, data_realizacao) VALUES
('Passeio ao Museu de Ciências', '2024-08-10'),
('Feira de Ciências', '2024-09-15'),
('Piquenique no Parque', '2024-10-05');

INSERT INTO Turmas (nome_turma, id_professor, horario) VALUES
('Turma A', 1, '08:00-12:00'),
('Turma B', 2, '13:00-17:00'),
('Turma C', 3, '10:00-14:00');

INSERT INTO Alunos (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais) VALUES
('Lucas Martins', '2015-03-12', 1, 'Fernanda Martins', '11988887777', 'fernanda.martins@email.com', 'Alergia a amendoim'),
('Sofia Almeida', '2014-07-25', 2, 'Paulo Almeida', '11977776666', 'paulo.almeida@email.com', 'Nenhuma'),
('Gabriel Souza', '2016-01-30', 3, 'Marcia Souza', '11966665555', 'marcia.souza@email.com', 'Usa óculos');

INSERT INTO Pagamentos (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status) VALUES
(1, '2024-07-01', 500.00, 'boleto', 'julho/2024', 'pago'),
(2, '2024-07-02', 500.00, 'cartao', 'julho/2024', 'pago'),
(3, '2024-07-03', 500.00, 'dinheiro', 'julho/2024', 'pendente');

INSERT INTO Presencas (id_aluno, data_presenca, presente) VALUES
(1, '2024-07-01', TRUE),
(2, '2024-07-01', FALSE),
(3, '2024-07-01', TRUE);

INSERT INTO Atividades_Alunos (id_atividade, id_aluno) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO Usuarios (login, senha, nivel_acesso, id_professor) VALUES
('ana.silva', 'senha123', 'admin', 1),
('carlos.souza', 'senha456', 'professor', 2),
('mariana.oliveira', 'senha789', 'professor', 3);

INSERT INTO Disciplinas (nome_disciplina, id_professor) VALUES
('Matemática', 1),
('Ciências', 2),
('História', 3);

INSERT INTO Notas (id_aluno, id_disciplina, valor_nota, data_avaliacao) VALUES
(1, 1, 9.0, '2024-07-10'),
(2, 2, 8.5, '2024-07-11'),
(3, 3, 7.8, '2024-07-12');

INSERT INTO Frequencias (id_aluno, id_disciplina, data_aula, presente) VALUES
(1, 1, '2024-07-01', TRUE),
(2, 2, '2024-07-01', FALSE),
(3, 3, '2024-07-01', TRUE);
