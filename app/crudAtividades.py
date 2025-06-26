from flask import request, jsonify, Blueprint
import Util.bd as bd

atividades_bp = Blueprint("atividades", __name__)


@atividades_bp.route("/atividades", methods=["GET"])
def listar_atividades():
    """
    Lista todas as atividades cadastradas.
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Lista de atividades retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_atividade:
                type: integer
              descricao:
                type: string
              data_realizacao:
                type: string
                format: date
      400:
        description: Erro ao buscar as atividades.
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
        cursor.execute("SELECT * FROM Atividade")
        atividades = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_atividade": atividade[0],
                        "descricao": atividade[1],
                        "data_realizacao": atividade[2],
                    }
                    for atividade in atividades
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@atividades_bp.route("/atividades", methods=["POST"])
def cadastrar_atividade():
    """
    Cadastra uma nova atividade.
    ---
    tags:
      - Atividades
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            data_realizacao:
              type: string
              format: date
    responses:
      201:
        description: Atividade cadastrada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao cadastrar a atividade.
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
            INSERT INTO Atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (
                data["descricao"],
                data["data_realizacao"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Atividade cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@atividades_bp.route("/atividades/<int:id_atividade>", methods=["PUT"])
def alterar_atividade(id_atividade):
    """
    Atualiza os dados de uma atividade existente.
    ---
    tags:
      - Atividades
    parameters:
      - name: id_atividade
        in: path
        required: true
        type: integer
        description: ID da atividade a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            data_realizacao:
              type: string
              format: date
    responses:
      200:
        description: Dados da atividade atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados da atividade.
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
            UPDATE Atividade
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (
                data["descricao"],
                data["data_realizacao"],
                id_atividade,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da atividade atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@atividades_bp.route("/atividades/<int:id_atividade>", methods=["DELETE"])
def excluir_atividade(id_atividade):
    """
    Exclui uma atividade existente.
    ---
    tags:
      - Atividades
    parameters:
      - name: id_atividade
        in: path
        required: true
        type: integer
        description: ID da atividade a ser excluída.
    responses:
      200:
        description: Atividade excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a atividade.
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
        cursor.execute("DELETE FROM Atividade WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        return jsonify({"message": "Atividade excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
