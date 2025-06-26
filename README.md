# Escola FAAT - Backend

## Descrição da Arquitetura

A aplicação backend da Escola FAAT é uma API RESTful desenvolvida em Python (Flask), estruturada em blueprints para cada domínio do sistema (alunos, professores, turmas, disciplinas, notas, frequências, pagamentos, atividades e usuários). O backend utiliza PostgreSQL como banco de dados e expõe endpoints CRUD para cada entidade. A documentação da API é gerada automaticamente via Swagger (Flasgger).

## Como Executar a Aplicação no Docker

1.  **Pré-requisitos**

    - Certifique-se de ter o Docker e o Docker-compose instalados na sua máquina.

    ```
    docker --version
    docker-compose --version
    ```

2.  **Clone o repositório**

    ```sh
    git clone <url-do-repositorio>
    cd projeto_escola_faat
    ```

3.  **Build e execução dos containers**

    - Com o Docker e o Docker-compose instalados, faça a build e a execução dos containers
    - OBS: Certifique-se de estar dentro da pasta raíz do projeto após fazer o clone do repositório

    ```
    docker-compose up --build
    ```

## Como Testar a Aplicação (APIS, CRUDS, etc)

4.  **Acessar a documentação Swagger**

    Você encontrará a documentação interativa de todos os endpoints, podendo testar as requisições diretamente pela interface.

    ```
    http://localhost:5000/apidocs
    ```

5.  **Exemplos de requisições para os Endpoints CRUD**

    As tabelas dependem de chaves estrangeiras (foreign keys). Com isso, teste os endpoints conforme a ordem de criação das tabelas (\projeto_escola_faat\bd\escola.sql) ou conforme a seguinte ordem:

    - Professor<br>
    - Atividade<br>
    - Turma<br>
    - Aluno<br>
    - Pagamento<br>
    - Presença<br>
    - Atividade_Aluno<br>
    - Usuário<br>
    - Disciplina<br>
    - Nota<br>
    - Frequencia<br>

    Utilize a ferramenta de testes de sua preferência (Postman, Insomnia, etc)<br>

    - **TABELA Professor (crudProfessores.py)**

      - Listar professores (método GET)

      ```
         GET http://localhost:5000/api/professores
      ```

      - Cadastrar um professor (método POST)

      ```
         POST http://localhost:5000/api/professores
      ```

      ```json
      {
        "nome_completo": "Carlos Souza",
        "email": "carlos@email.com",
        "telefone": "11988887777"
      }
      ```

      - Atualizar o cadastro de um professor (método PUT)

      ```
         PUT http://localhost:5000/api/professores/1
      ```

      ```json
      {
        "nome_completo": "Carlos Souza",
        "email": "carlos@email.com",
        "telefone": "11988887777"
      }
      ```

      - Excluir o cadastro de um professor (método DELETE)

      ```
         DELETE http://localhost:5000/api/professores/1
      ```

    - **TABELA Atividade (crudAtividades.py)**

      - Listar atividades (método GET)

      ```
         GET http://localhost:5000/api/atividades
      ```

      - Cadastrar uma atividade (método POST)

      ```
         POST http://localhost:5000/api/atividades
      ```

      ```json
      {
        "descricao": "Passeio ao museu",
        "data_realizacao": "2024-07-10"
      }
      ```

      - Atualizar uma atividade (método PUT)

      ```
         PUT http://localhost:5000/api/atividades/1
      ```

      ```json
      {
        "descricao": "Passeio ao parque",
        "data_realizacao": "2024-07-15"
      }
      ```

      - Excluir uma atividade (método DELETE)

      ```
         DELETE http://localhost:5000/api/atividades/1
      ```

    - **TABELA Turma (crudTurmas.py)**

      - Listar turmas (método GET)

      ```
         GET http://localhost:5000/api/turmas
      ```

      - Cadastrar uma turma (método POST)

      ```
         POST http://localhost:5000/api/turmas
      ```

      ```json
      {
        "nome_turma": "Turma A",
        "id_professor": 1,
        "horario": "08:00-12:00"
      }
      ```

      - Atualizar uma turma (método PUT)

      ```
         PUT http://localhost:5000/api/turmas/1
      ```

      ```json
      {
        "nome_turma": "Turma A - Atualizada",
        "id_professor": 1,
        "horario": "13:00-17:00"
      }
      ```

      - Excluir uma turma cadastrada (método DELETE)

      ```
         DELETE http://localhost:5000/api/turmas/1
      ```

    - **TABELA Alunos (crudAlunos.py)**

      - Listar alunos (método GET)

      ```
         GET http://localhost:5000/api/alunos
      ```

      - Cadastrar um aluno (método POST)

      ```
         POST http://localhost:5000/api/alunos
      ```

      ```json
      {
        "nome_completo": "João da Silva",
        "data_nascimento": "2010-05-10",
        "id_turma": 2,
        "nome_responsavel": "Maria Silva",
        "telefone_responsavel": "11999999999",
        "email_responsavel": "maria@email.com",
        "informacoes_adicionais": "Nenhuma"
      }
      ```

      - Atualizar um aluno (método PUT)

      ```
         PUT http://localhost:5000/api/alunos/1
      ```

      ```json
      {
        "nome_completo": "João da Silva",
        "data_nascimento": "2010-05-10",
        "id_turma": 2,
        "nome_responsavel": "Maria Silva",
        "telefone_responsavel": "11999999999",
        "email_responsavel": "maria@email.com",
        "informacoes_adicionais": "Atualizado"
      }
      ```

      - Excluir um aluno cadastrado (método DELETE)

      ```
         DELETE http://localhost:5000/api/alunos/1
      ```

    - **TABELA Pagamento (crudPagamentos.py)**

      - Listar pagamentos (método GET)

      ```
        GET http://localhost:5000/api/pagamentos
      ```

      - Cadastrar um pagamento (método POST)

      ```
        POST http://localhost:5000/api/pagamentos
      ```

      ```json
      {
        "id_aluno": 1,
        "data_pagamento": "2024-06-25",
        "valor_pago": 500.0,
        "forma_pagamento": "boleto",
        "referencia": "junho/2024",
        "status": "pago"
      }
      ```

      - Atualizar um pagamento (método PUT)

      ```
        PUT http://localhost:5000/api/pagamentos/1
      ```

      ```json
      {
        "id_aluno": 1,
        "data_pagamento": "2024-06-26",
        "valor_pago": 550.0,
        "forma_pagamento": "cartao",
        "referencia": "junho/2024",
        "status": "pago"
      }
      ```

      - Excluir um pagamento cadastrado (método DELETE)

      ```
        DELETE http://localhost:5000/api/pagamentos/1
      ```

    - **TABELA Presenca (crudPresencas.py)**

      - Listar presenças (método GET)

      ```
        GET http://localhost:5000/api/presencas
      ```

      - Cadastrar uma presença (método POST)

      ```
        POST http://localhost:5000/api/presencas
      ```

      ```json
      {
        "id_aluno": 1,
        "data_presenca": "2024-06-26",
        "presente": true
      }
      ```

      - Atualizar uma presença (método PUT)

      ```
        PUT http://localhost:5000/api/presencas/1
      ```

      ```json
      {
        "id_aluno": 1,
        "data_presenca": "2024-06-27",
        "presente": false
      }
      ```

      - Excluir uma presença (método DELETE)

      ```
        DELETE http://localhost:5000/api/presencas/1
      ```

6.  **Observações**

    - O backend faz log das operações em escola_infantil.log.

    - Para atualizar dependências Python, edite o requirements.txt e reconstrua a imagem com:

    ```
    docker-compose up --build
    ```
