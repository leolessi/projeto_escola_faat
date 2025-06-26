from flask import Blueprint, request, jsonify
import Util.bd as bd
import logging


logger = logging.getLogger(__name__)
professores_bp = Blueprint("professores", __name__)


@professores_bp.route("/professores", methods=["GET"])
def listar_professores():
    """
    Lista todos os professores cadastrados.
    ---
    tags:
      - Professores
    responses:
      200:
        description: Lista de professores retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_professor:
                type: integer
              nome_completo:
                type: string
              email:
                type: string
              telefone:
                type: string
      400:
        description: Erro ao buscar os professores.
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
        cursor.execute("SELECT * FROM Professor")
        professores = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_professor": professor[0],
                        "nome_completo": professor[1],
                        "email": professor[2],
                        "telefone": professor[3],
                    }
                    for professor in professores
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@professores_bp.route("/professores", methods=["POST"])
def cadastrar_professor():
    """
    Cadastra um novo professor.
    ---
    tags:
      - Professores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            email:
              type: string
            telefone:
              type: string
    responses:
      201:
        description: Professor cadastrado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao criar professor.
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
            INSERT INTO Professor (nome_completo, email, telefone)
            VALUES (%s, %s, %s)
            """,
            (
                data["nome_completo"],
                data["email"],
                data["telefone"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Professor cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@professores_bp.route("/professores/<int:id_professor>", methods=["PUT"])
def alterar_professor(id_professor):
    """
    Atualiza os dados de um professor existente.
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        required: true
        type: integer
        description: ID do professor a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            email:
              type: string
            telefone:
              type: string
    responses:
      200:
        description: Dados do professor atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados do professor.
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
            UPDATE Professor
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s
            """,
            (
                data["nome_completo"],
                data["email"],
                data["telefone"],
                id_professor,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados do professor atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@professores_bp.route("/professores/<int:id_professor>", methods=["DELETE"])
def excluir_professor(id_professor):
    """
    Exclui um professor existente.
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        required: true
        type: integer
        description: ID do professor a ser excluído.
    responses:
      200:
        description: Professor excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir o professor.
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
        cursor.execute("DELETE FROM Professor WHERE id_professor = %s", (id_professor,))
        conn.commit()
        return jsonify({"message": "Professor excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
