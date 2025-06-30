from flask import Blueprint, request, jsonify
from Util import bd

atividade_aluno_bp = Blueprint("atividade_aluno", __name__)


@atividade_aluno_bp.route("/atividade_aluno", methods=["GET"])
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
        cursor.execute("SELECT * FROM Atividades_Alunos")
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


@atividade_aluno_bp.route("/atividade_aluno/alunos/<int:id_aluno>", methods=["GET"])
def listar_atividades_por_aluno(id_aluno):
    """
    Lista todas as atividades de um aluno específico.
    ---
    tags:
      - Atividade_Aluno
    parameters:
      - name: id_aluno
        in: path
        required: true
        type: integer
        description: ID do aluno
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
      400:
        description: Erro ao buscar as atividades.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Erro de conexão com o banco de dados"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_atividade FROM Atividades_Alunos WHERE id_aluno = %s",
            (id_aluno,),
        )
        atividades = cursor.fetchall()
        return (
            jsonify([{"id_atividade": atividade[0]} for atividade in atividades]),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@atividade_aluno_bp.route(
    "/atividade_aluno/atividade/<int:id_atividade>", methods=["GET"]
)
def listar_alunos_por_atividade(id_atividade):
    """
    Lista todos os alunos de uma atividade específica.
    ---
    tags:
      - Atividade_Aluno
    parameters:
      - name: id_atividade
        in: path
        required: true
        type: integer
        description: ID da atividade
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
      400:
        description: Erro ao buscar os alunos.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Erro de conexão com o banco de dados"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id_aluno FROM Atividades_Alunos WHERE id_atividade = %s",
            (id_atividade,),
        )
        alunos = cursor.fetchall()
        return jsonify([{"id_aluno": aluno[0]} for aluno in alunos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@atividade_aluno_bp.route("/atividade_aluno", methods=["POST"])
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
            INSERT INTO Atividades_Alunos (id_atividade, id_aluno)
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


@atividade_aluno_bp.route(
    "/atividade_aluno/<int:id_atividade>/<int:id_aluno>", methods=["PUT"]
)
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
            UPDATE Atividades_Alunos
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


@atividade_aluno_bp.route(
    "/atividade_aluno/<int:id_atividade>/<int:id_aluno>", methods=["DELETE"]
)
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
            "DELETE FROM Atividades_Alunos WHERE id_atividade = %s AND id_aluno = %s",
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
