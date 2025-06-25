from flask import Blueprint, request, jsonify
import Util.bd as bd

disciplinas_bp = Blueprint("disciplinas", __name__)

@disciplinas_bp.route("/disciplinas", methods=["GET"])
def listar_disciplinas():
    """
    Lista todas as disciplinas cadastradas.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Disciplina")
        disciplinas = cursor.fetchall()
        return (
            jsonify([
                {
                    "id_disciplina": d[0],
                    "nome_disciplina": d[1],
                    "id_professor": d[2]
                } for d in disciplinas
            ]),
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
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Disciplina WHERE id_disciplina = %s", (id_disciplina,))
        d = cursor.fetchone()
        if d is None:
            return jsonify({"error": "Disciplina não encontrada"}), 404
        return (
            jsonify({
                "id_disciplina": d[0],
                "nome_disciplina": d[1],
                "id_professor": d[2]
            }),
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
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Disciplina WHERE id_disciplina = %s", (id_disciplina,))
        conn.commit()
        return jsonify({"message": "Disciplina excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()