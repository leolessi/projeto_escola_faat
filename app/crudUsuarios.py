from flask import Blueprint, request, jsonify
from Util import bd

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    """
    Lista todos os usuários cadastrados.
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuários retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_usuario:
                type: integer
              login:
                type: string
              senha:
                type: string
              nivel_acesso:
                type: string
              id_professor:
                type: integer
      400:
        description: Erro ao buscar os usuários.
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
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_usuario": usuario[0],
                        "login": usuario[1],
                        "senha": usuario[2],
                        "nivel_acesso": usuario[3],
                        "id_professor": usuario[4],
                    }
                    for usuario in usuarios
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["GET"])
def buscar_usuario(id_usuario):
    """
    Busca um usuário pelo ID.
    ---
    tags:
      - Usuarios
    parameters:
      - name: id_usuario
        in: path
        required: true
        type: integer
        description: ID do usuário a ser buscado.
    responses:
      200:
        description: Usuário encontrado com sucesso.
        schema:
          type: object
          properties:
            id_usuario:
              type: integer
            login:
              type: string
            senha:
              type: string
            nivel_acesso:
              type: string
            id_professor:
              type: integer
      404:
        description: Usuário não encontrado.
      500:
        description: Erro de conexão com o banco de dados.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        if usuario is None:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return (
            jsonify(
                {
                    "id_usuario": usuario[0],
                    "login": usuario[1],
                    "senha": usuario[2],
                    "nivel_acesso": usuario[3],
                    "id_professor": usuario[4],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@usuarios_bp.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    """
    Cadastra um novo usuário.
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            login:
              type: string
            senha:
              type: string
            nivel_acesso:
              type: string
            id_professor:
              type: integer
    responses:
      201:
        description: Usuário cadastrado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao cadastrar o usuário.
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
            INSERT INTO Usuarios (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["login"],
                data["senha"],
                data["nivel_acesso"],
                data.get("id_professor"),
            ),
        )
        conn.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def alterar_usuario(id_usuario):
    """
    Atualiza os dados de um usuário existente.
    ---
    tags:
      - Usuarios
    parameters:
      - name: id_usuario
        in: path
        required: true
        type: integer
        description: ID do usuário a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            login:
              type: string
            senha:
              type: string
            nivel_acesso:
              type: string
            id_professor:
              type: integer
    responses:
      200:
        description: Dados do usuário atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados do usuário.
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
            UPDATE Usuarios
            SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s
            WHERE id_usuario = %s
            """,
            (
                data["login"],
                data["senha"],
                data["nivel_acesso"],
                data.get("id_professor"),
                id_usuario,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados do usuário atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def excluir_usuario(id_usuario):
    """
    Exclui um usuário existente.
    ---
    tags:
      - Usuarios
    parameters:
      - name: id_usuario
        in: path
        required: true
        type: integer
        description: ID do usuário a ser excluído.
    responses:
      200:
        description: Usuário excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir o usuário.
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
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
