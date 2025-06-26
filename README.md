# Escola FAAT - Backend

## Descrição da Arquitetura

A aplicação backend da Escola FAAT é uma API RESTful desenvolvida em Python (Flask), estruturada em blueprints para cada domínio do sistema (alunos, professores, turmas, disciplinas, notas, frequências, pagamentos, atividades e usuários). O backend utiliza PostgreSQL como banco de dados e expõe endpoints CRUD para cada entidade. A documentação da API é gerada automaticamente via Swagger (Flasgger).

## Como Executar a Aplicação no Docker

1. **Pré-requisitos**

   - Certifique-se de ter o Docker e o Docker-compose instalados na sua máquina.

   ```
   docker --version
   docker-compose --version
   ```

2. **Clone o repositório**

   ```sh
   git clone <url-do-repositorio>
   cd projeto_escola_faat
   ```

3. **Build e execução dos containers**

   - Com o Docker e o Docker-compose instalados, faça a build e a execução dos containers
   - OBS: Certifique-se de estar dentro da pasta raíz do projeto após fazer o clone do repositório

   ```sh
   docker-compose up --build
   ```

4. **Acessar a documentação Swagger**

   ```
   http://localhost:5000/apidocs
   ```

5. Exemplos de requisições para os Endpoints CRUD
   Utilize a ferramenta de testes de sua preferência (Postman, Insomnia, etc)

   - Tabela Alunos (crudAlunos.py)
     -> Listar alunos (método GET)
     /api/alunos
     -- Cadastrar um aluno (método POST)
     /api/alunos
     {
     "nome_completo": "João da Silva",
     "data_nascimento": "2010-05-10",
     "id_turma": 2,
     "nome_responsavel": "Maria Silva",
     "telefone_responsavel": "11999999999",
     "email_responsavel": "maria@email.com",
     "informacoes_adicionais": "Nenhuma"
     }
     -- Atualizar cadastro do aluno (método PUT)
     /api/alunos/1
     {
     "nome_completo": "João da Silva",
     "data_nascimento": "2010-05-10",
     "id_turma": 2,
     "nome_responsavel": "Maria Silva",
     "telefone_responsavel": "11999999999",
     "email_responsavel": "maria@email.com",
     "informacoes_adicionais": "Atualizado"
     }
     -- Excluir um aluno cadastrado (método DELETE)
     /api/alunos/1
