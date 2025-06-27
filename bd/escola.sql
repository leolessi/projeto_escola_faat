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