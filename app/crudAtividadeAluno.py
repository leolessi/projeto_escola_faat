from flask import Flask, request, jsonify
import Util.bd as bd
from flasgger import Swagger

app = Flask(__name__)

swagger = Swagger(app)


@app.route("/atividade_aluno", methods=["GET"])
def listar_atividade_aluno():
    """
    Lista todas as associações entre atividades e alunos.
    ---
    tags:
      - Atividade_Aluno
    responses:
      200:
        description: Lista de associações retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_atividade:
                type: integer
              id_aluno:
                type: integer
      400:
        description: Erro ao buscar as associações.
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
        cursor.execute("SELECT * FROM Atividade_Aluno")
        atividade_aluno = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_atividade": item[0],
                        "id_aluno": item[1],
                    }
                    for item in atividade_aluno
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividade_aluno", methods=["POST"])
def cadastrar_atividade_aluno():
    """
    Associa uma atividade a um aluno.
    ---
    tags:
      - Atividade_Aluno
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_atividade:
              type: integer
            id_aluno:
              type: integer
    responses:
      201:
        description: Atividade associada ao aluno com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao associar a atividade ao aluno.
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
            INSERT INTO Atividade_Aluno (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (
                data["id_atividade"],
                data["id_aluno"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Atividade associada ao aluno com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividade_aluno/<int:id_atividade>/<int:id_aluno>", methods=["PUT"])
def atualizar_atividade_aluno(id_atividade, id_aluno):
    """
    Atualiza a associação entre uma atividade e um aluno.
    ---
    tags:
      - Atividade_Aluno
    parameters:
      - name: id_atividade
        in: path
        required: true
        type: integer
        description: ID da atividade a ser atualizada.
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
            novo_id_atividade:
              type: integer
              description: Novo ID da atividade.
            novo_id_aluno:
              type: integer
              description: Novo ID do aluno.
    responses:
      200:
        description: Associação entre atividade e aluno atualizada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar a associação.
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
            UPDATE Atividade_Aluno
            SET id_atividade = %s, id_aluno = %s
            WHERE id_atividade = %s AND id_aluno = %s
            """,
            (
                data["novo_id_atividade"],
                data["novo_id_aluno"],
                id_atividade,
                id_aluno,
            ),
        )
        conn.commit()
        return (
            jsonify(
                {"message": "Associação entre atividade e aluno atualizada com sucesso"}
            ),
            200,
        )
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividade_aluno/<int:id_atividade>/<int:id_aluno>", methods=["DELETE"])
def excluir_atividade_aluno(id_atividade, id_aluno):
    """
    Exclui a associação entre uma atividade e um aluno.
    ---
    tags:
      - Atividade_Aluno
    parameters:
      - name: id_atividade
        in: path
        required: true
        type: integer
        description: ID da atividade a ser desassociada.
      - name: id_aluno
        in: path
        required: true
        type: integer
        description: ID do aluno a ser desassociado.
    responses:
      200:
        description: Associação entre atividade e aluno excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a associação.
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
        cursor.execute(
            "DELETE FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s",
            (id_atividade, id_aluno),
        )
        conn.commit()
        return (
            jsonify(
                {"message": "Associação entre atividade e aluno excluída com sucesso"}
            ),
            200,
        )
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
