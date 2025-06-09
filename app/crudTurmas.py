from flask import Flask, request, jsonify, Blueprint
import Util.bd as bd
from flasgger import Swagger

# app = Flask(__name__)

# swagger = Swagger(app)
turmas_bp = Blueprint("turmas", __name__)


@turmas_bp.route("/turmas", methods=["GET"])
def listar_turmas():
    """
    Lista todas as turmas cadastradas.
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_turma:
                type: integer
              nome_turma:
                type: string
              id_professor:
                type: integer
              horario:
                type: string
      400:
        description: Erro ao buscar as turmas.
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
        cursor.execute("SELECT * FROM Turma")
        turmas = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_turma": turma[0],
                        "nome_turma": turma[1],
                        "id_professor": turma[2],
                        "horario": turma[3],
                    }
                    for turma in turmas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@turmas_bp.route("/turmas", methods=["POST"])
def cadastrar_turma():
    """
    Cadastra uma nova turma.
    ---
    tags:
      - Turmas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_turma:
              type: string
            id_professor:
              type: integer
            horario:
              type: string
    responses:
      201:
        description: Turma cadastrada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao cadastrar a turma.
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
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (
                data["nome_turma"],
                data.get("id_professor"),
                data["horario"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Turma cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@turmas_bp.route("/turmas/<int:id_turma>", methods=["PUT"])
def alterar_turma(id_turma):
    """
    Atualiza os dados de uma turma existente.
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        required: true
        type: integer
        description: ID da turma a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_turma:
              type: string
            id_professor:
              type: integer
            horario:
              type: string
    responses:
      200:
        description: Dados da turma atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados da turma.
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
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (
                data["nome_turma"],
                data.get("id_professor"),
                data["horario"],
                id_turma,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da turma atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@turmas_bp.route("/turmas/<int:id_turma>", methods=["DELETE"])
def excluir_turma(id_turma):
    """
    Exclui uma turma existente.
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        required: true
        type: integer
        description: ID da turma a ser excluída.
    responses:
      200:
        description: Turma excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a turma.
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
        cursor.execute("DELETE FROM Turma WHERE id_turma = %s", (id_turma,))
        conn.commit()
        return jsonify({"message": "Turma excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)
