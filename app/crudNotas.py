from flask import Blueprint, request, jsonify
from app.Util import bd

notas_bp = Blueprint("notas", __name__)


@notas_bp.route("/notas", methods=["GET"])
def listar_notas():
    """
    Lista todas as notas cadastradas.
    ---
    tags:
      - Notas
    responses:
      200:
        description: Lista de notas retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_nota:
                type: integer
              id_aluno:
                type: integer
              id_disciplina:
                type: integer
              valor_nota:
                type: number
                format: float
              data_avaliacao:
                type: string
                format: date
      400:
        description: Erro ao buscar as notas.
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
        cursor.execute("SELECT * FROM Nota")
        notas = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_nota": n[0],
                        "id_aluno": n[1],
                        "id_disciplina": n[2],
                        "valor_nota": float(n[3]),
                        "data_avaliacao": n[4].isoformat() if n[4] else None,
                    }
                    for n in notas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@notas_bp.route("/notas/<int:id_nota>", methods=["GET"])
def buscar_nota(id_nota):
    """
    Busca uma nota pelo ID.
    ---
    tags:
      - Notas
    parameters:
      - name: id_nota
        in: path
        required: true
        type: integer
        description: ID da nota a ser buscada.
    responses:
      200:
        description: Nota encontrada com sucesso.
        schema:
          type: object
          properties:
            id_nota:
              type: integer
            id_aluno:
              type: integer
            id_disciplina:
              type: integer
            valor_nota:
              type: number
              format: float
            data_avaliacao:
              type: string
              format: date
      404:
        description: Nota não encontrada.
      500:
        description: Erro de conexão com o banco de dados.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Nota WHERE id_nota = %s", (id_nota,))
        n = cursor.fetchone()
        if n is None:
            return jsonify({"error": "Nota não encontrada"}), 404
        return (
            jsonify(
                {
                    "id_nota": n[0],
                    "id_aluno": n[1],
                    "id_disciplina": n[2],
                    "valor_nota": float(n[3]),
                    "data_avaliacao": n[4].isoformat() if n[4] else None,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@notas_bp.route("/notas", methods=["POST"])
def cadastrar_nota():
    """
    Cadastra uma nova nota.
    ---
    tags:
      - Notas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            id_disciplina:
              type: integer
            valor_nota:
              type: number
              format: float
            data_avaliacao:
              type: string
              format: date
    responses:
      201:
        description: Nota cadastrada com sucesso.
      400:
        description: Erro ao criar nota.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Nota (id_aluno, id_disciplina, valor_nota, data_avaliacao) VALUES (%s, %s, %s, %s)",
            (
                data["id_aluno"],
                data["id_disciplina"],
                data["valor_nota"],
                data["data_avaliacao"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Nota cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@notas_bp.route("/notas/<int:id_nota>", methods=["PUT"])
def alterar_nota(id_nota):
    """
    Atualiza os dados de uma nota existente.
    ---
    tags:
      - Notas
    parameters:
      - name: id_nota
        in: path
        required: true
        type: integer
        description: ID da nota a ser atualizada.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            id_disciplina:
              type: integer
            valor_nota:
              type: number
              format: float
            data_avaliacao:
              type: string
              format: date
    responses:
      200:
        description: Dados da nota atualizados com sucesso.
      400:
        description: Erro ao atualizar os dados da nota.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Nota SET id_aluno = %s, id_disciplina = %s, valor_nota = %s, data_avaliacao = %s WHERE id_nota = %s",
            (
                data["id_aluno"],
                data["id_disciplina"],
                data["valor_nota"],
                data["data_avaliacao"],
                id_nota,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da nota atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@notas_bp.route("/notas/<int:id_nota>", methods=["DELETE"])
def excluir_nota(id_nota):
    """
    Exclui uma nota existente.
    ---
    tags:
      - Notas
    parameters:
      - name: id_nota
        in: path
        required: true
        type: integer
        description: ID da nota a ser excluída.
    responses:
      200:
        description: Nota excluída com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir a nota.
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
        cursor.execute("DELETE FROM Nota WHERE id_nota = %s", (id_nota,))
        conn.commit()
        return jsonify({"message": "Nota excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@notas_bp.route("/notas/aluno/<int:id_aluno>", methods=["GET"])
def buscar_notas_por_aluno(id_aluno):
    """
    Busca todas as notas de um aluno pelo ID do aluno.
    ---
    tags:
      - Notas
    parameters:
      - name: id_aluno
        in: path
        required: true
        type: integer
        description: ID do aluno a ser buscado.
    responses:
      200:
        description: Lista de notas do aluno retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_nota:
                type: integer
              id_aluno:
                type: integer
              id_disciplina:
                type: integer
              valor_nota:
                type: number
                format: float
              data_avaliacao:
                type: string
                format: date
      404:
        description: Nenhuma nota encontrada para este aluno.
      500:
        description: Erro de conexão com o banco de dados.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Nota WHERE id_aluno = %s", (id_aluno,))
        notas = cursor.fetchall()
        if not notas:
            return jsonify({"error": "Nenhuma nota encontrada para este aluno"}), 404
        return (
            jsonify(
                [
                    {
                        "id_nota": n[0],
                        "id_aluno": n[1],
                        "id_disciplina": n[2],
                        "valor_nota": float(n[3]),
                        "data_avaliacao": n[4].isoformat() if n[4] else None,
                    }
                    for n in notas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
