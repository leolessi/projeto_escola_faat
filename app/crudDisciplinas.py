from flask import Blueprint, request, jsonify
import Util.bd as bd

disciplinas_bp = Blueprint("disciplinas", __name__)


@disciplinas_bp.route("/disciplinas", methods=["GET"])
def listar_disciplinas():
    """
    Lista todas as disciplinas cadastradas.
    ---
    tags:
      - Disciplinas
    responses:
      200:
        description: Lista de disciplinas retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_disciplina:
                type: integer
              nome_disciplina:
                type: string
              id_professor:
                type: integer
      400:
        description: Erro ao buscar as disciplinas.
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
        cursor.execute("SELECT * FROM Disciplina")
        disciplinas = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_disciplina": d[0],
                        "nome_disciplina": d[1],
                        "id_professor": d[2],
                    }
                    for d in disciplinas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@disciplinas_bp.route("/disciplinas/<int:id_disciplina>", methods=["GET"])
def buscar_disciplina(id_disciplina):
    """
    Busca uma disciplina pelo ID.
    ---
    tags:
      - Disciplinas
    parameters:
      - name: id_disciplina
        in: path
        required: true
        type: integer
        description: ID da disciplina a ser buscada.
    responses:
      200:
        description: Disciplina encontrada com sucesso.
        schema:
          type: object
          properties:
            id_disciplina:
              type: integer
            nome_disciplina:
              type: string
            id_professor:
              type: integer
      404:
        description: Disciplina não encontrada.
      500:
        description: Erro de conexão com o banco de dados.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM Disciplina WHERE id_disciplina = %s", (id_disciplina,)
        )
        d = cursor.fetchone()
        if d is None:
            return jsonify({"error": "Disciplina não encontrada"}), 404
        return (
            jsonify(
                {"id_disciplina": d[0], "nome_disciplina": d[1], "id_professor": d[2]}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@disciplinas_bp.route("/disciplinas", methods=["POST"])
def cadastrar_disciplina():
    """
    Cadastra uma nova disciplina.
    ---
    tags:
      - Disciplinas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_disciplina:
              type: string
            id_professor:
              type: integer
    responses:
      201:
        description: Disciplina cadastrada com sucesso.
      400:
        description: Erro ao criar disciplina.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Disciplina (nome_disciplina, id_professor) VALUES (%s, %s)",
            (data["nome_disciplina"], data.get("id_professor")),
        )
        conn.commit()
        return jsonify({"message": "Disciplina cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@disciplinas_bp.route("/disciplinas/<int:id_disciplina>", methods=["PUT"])
def alterar_disciplina(id_disciplina):
    """
    Atualiza os dados de uma disciplina existente.
    ---
    tags:
      - Disciplinas
    parameters:
      - name: id_disciplina
        in: path
        required: true
        type: integer
        description: ID da disciplina a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_disciplina:
              type: string
            id_professor:
              type: integer
    responses:
      200:
        description: Dados da disciplina atualizados com sucesso.
      400:
        description: Erro ao atualizar os dados da disciplina.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Disciplina SET nome_disciplina = %s, id_professor = %s WHERE id_disciplina = %s",
            (data["nome_disciplina"], data.get("id_professor"), id_disciplina),
        )
        conn.commit()
        return jsonify({"message": "Dados da disciplina atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@disciplinas_bp.route("/disciplinas/<int:id_disciplina>", methods=["DELETE"])
def excluir_disciplina(id_disciplina):
    """
    Exclui uma disciplina existente.
    ---
    tags:
      - Disciplinas
    parameters:
      - name: id_disciplina
        in: path
        required: true
        type: integer
        description: ID da disciplina a ser excluída.
    responses:
      200:
        description: Disciplina excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a disciplina.
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
        cursor.execute(
            "DELETE FROM Disciplina WHERE id_disciplina = %s", (id_disciplina,)
        )
        conn.commit()
        return jsonify({"message": "Disciplina excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
