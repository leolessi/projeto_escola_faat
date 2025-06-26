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

   ```sh
   docker-compose up --build
   ```
