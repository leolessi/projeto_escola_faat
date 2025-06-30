from flask import Blueprint, request, jsonify
from app.Util import bd

presencas_bp = Blueprint("presencas", __name__)


@presencas_bp.route("/presencas", methods=["GET"])
def listar_presencas():
    """
    Lista todas as presenças cadastradas.
    ---
    tags:
      - Presencas
    responses:
      200:
        description: Lista de presenças retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_presenca:
                type: integer
              id_aluno:
                type: integer
              data_presenca:
                type: string
                format: date
              presente:
                type: boolean
      400:
        description: Erro ao buscar as presenças.
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
        cursor.execute("SELECT * FROM Presenca")
        presencas = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_presenca": presenca[0],
                        "id_aluno": presenca[1],
                        "data_presenca": presenca[2],
                        "presente": bool(presenca[3]),
                    }
                    for presenca in presencas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@presencas_bp.route("/presencas", methods=["POST"])
def cadastrar_presenca():
    """
    Cadastra uma nova presença.
    ---
    tags:
      - Presencas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_presenca:
              type: string
              format: date
            presente:
              type: boolean
    responses:
      201:
        description: Presença cadastrada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao cadastrar a presença.
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
            INSERT INTO Presenca (id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s)
            """,
            (
                data["id_aluno"],
                data["data_presenca"],
                data["presente"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Presença cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@presencas_bp.route("/presencas/<int:id_presenca>", methods=["PUT"])
def alterar_presenca(id_presenca):
    """
    Atualiza os dados de uma presença existente.
    ---
    tags:
      - Presencas
    parameters:
      - name: id_presenca
        in: path
        required: true
        type: integer
        description: ID da presença a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_presenca:
              type: string
              format: date
            presente:
              type: boolean
    responses:
      200:
        description: Dados da presença atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados da presença.
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
            UPDATE Presenca
            SET id_aluno = %s, data_presenca = %s, presente = %s
            WHERE id_presenca = %s
            """,
            (
                data["id_aluno"],
                data["data_presenca"],
                data["presente"],
                id_presenca,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da presença atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@presencas_bp.route("/presencas/<int:id_presenca>", methods=["DELETE"])
def excluir_presenca(id_presenca):
    """
    Exclui uma presença existente.
    ---
    tags:
      - Presencas
    parameters:
      - name: id_presenca
        in: path
        required: true
        type: integer
        description: ID da presença a ser excluída.
    responses:
      200:
        description: Presença excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a presença.
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
        cursor.execute("DELETE FROM Presenca WHERE id_presenca = %s", (id_presenca,))
        conn.commit()
        return jsonify({"message": "Presença excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
