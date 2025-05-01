from flask import Flask, request, jsonify
import Util.bd as bd
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)


@app.route("/alunos", methods=["GET"])
def listar_alunos():
    """
    Lista todos os alunos.
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_aluno:
                type: integer
              nome_completo:
                type: string
              data_nascimento:
                type: string
                format: date
              id_turma:
                type: integer
              nome_responsavel:
                type: string
              telefone_responsavel:
                type: string
              email_responsavel:
                type: string
              informacoes_adicionais:
                type: string
      400:
        description: Erro ao buscar os alunos.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Aluno")
        alunos = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_aluno": aluno[0],
                        "nome_completo": aluno[1],
                        "data_nascimento": aluno[2],
                        "id_turma": aluno[3],
                        "nome_responsavel": aluno[4],
                        "telefone_responsavel": aluno[5],
                        "email_responsavel": aluno[6],
                        "informacoes_adicionais": aluno[7],
                    }
                    for aluno in alunos
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    """
    Cadastra um novo aluno.
    ---
    tags:
      - Alunos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            data_nascimento:
              type: string
              format: date
            id_turma:
              type: integer
            nome_responsavel:
              type: string
            telefone_responsavel:
              type: string
            email_responsavel:
              type: string
            informacoes_adicionais:
              type: string
        responses:
      201:
        description: Aluno cadastrado com sucesso.
      400:
        description: Erro ao criar aluno.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Aluno (nome_completo, data_nascimento, id_turma, nome_responsavel, telefone_responsavel, email_responsavel, informacoes_adicionais)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data["nome_completo"],
                data["data_nascimento"],
                data.get("id_turma"),
                data["nome_responsavel"],
                data["telefone_responsavel"],
                data["email_responsavel"],
                data.get("informacoes_adicionais"),
            ),
        )
        conn.commit()
        return jsonify({"message": "Aluno cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/alunos/<int:id_aluno>", methods=["PUT"])
def alterar_aluno(id_aluno):
    """
    Atualiza os dados de um aluno cadastrado.
    ---
    tags:
      - Alunos
    parameters:
      - name: id_aluno
        in: path
        required: true
        type: integer
        description: ID do aluno a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            data_nascimento:
              type: string
              format: date
            id_turma:
              type: integer
            nome_responsavel:
              type: string
            telefone_responsavel:
              type: string
            email_responsavel:
              type: string
            informacoes_adicionais:
              type: string
    responses:
      200:
        description: Dados do aluno atualizados com sucesso.
      400:
        description: Erro ao atualizar os dados do aluno.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Aluno
            SET nome_completo = %s, data_nascimento = %s, id_turma = %s, nome_responsavel = %s, telefone_responsavel = %s, email_responsavel = %s, informacoes_adicionais = %s
            WHERE id_aluno = %s
            """,
            (
                data["nome_completo"],
                data["data_nascimento"],
                data.get("id_turma"),
                data["nome_responsavel"],
                data["telefone_responsavel"],
                data["email_responsavel"],
                data.get("informacoes_adicionais"),
                id_aluno,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados do aluno atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/alunos/<int:id_aluno>", methods=["DELETE"])
def excluir_aluno(id_aluno):
    """
    Exclui um aluno existente.
    ---
    tags:
      - Alunos
    parameters:
      - name: id_aluno
        in: path
        required: true
        type: integer
        description: ID do aluno a ser excluído.
    responses:
      200:
        description: Aluno excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir o aluno.
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro de conexão com o banco de dados.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Aluno WHERE id_aluno = %s", (id_aluno,))
        conn.commit()
        return jsonify({"message": "Aluno excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
