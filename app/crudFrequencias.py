from flask import Blueprint, request, jsonify
import Util.bd as bd

frequencias_bp = Blueprint("frequencias", __name__)


@frequencias_bp.route("/frequencias", methods=["GET"])
def listar_frequencias():
    """
    Lista todas as frequências cadastradas.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Frequencia")
        frequencias = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_frequencia": f[0],
                        "id_aluno": f[1],
                        "id_disciplina": f[2],
                        "data_aula": f[3].isoformat() if f[3] else None,
                        "presente": f[4],
                    }
                    for f in frequencias
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@frequencias_bp.route("/frequencias/aluno/<int:id_aluno>", methods=["GET"])
def buscar_frequencias_por_aluno(id_aluno):
    """
    Busca todas as frequências de um aluno pelo ID do aluno.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Frequencia WHERE id_aluno = %s", (id_aluno,))
        frequencias = cursor.fetchall()
        if not frequencias:
            return (
                jsonify({"error": "Nenhuma frequência encontrada para este aluno"}),
                404,
            )
        return (
            jsonify(
                [
                    {
                        "id_frequencia": f[0],
                        "id_aluno": f[1],
                        "id_disciplina": f[2],
                        "data_aula": f[3].isoformat() if f[3] else None,
                        "presente": f[4],
                    }
                    for f in frequencias
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@frequencias_bp.route("/frequencias/<int:id_frequencia>", methods=["GET"])
def buscar_frequencia(id_frequencia):
    """
    Busca uma frequência pelo ID.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM Frequencia WHERE id_frequencia = %s", (id_frequencia,)
        )
        f = cursor.fetchone()
        if f is None:
            return jsonify({"error": "Frequência não encontrada"}), 404
        return (
            jsonify(
                {
                    "id_frequencia": f[0],
                    "id_aluno": f[1],
                    "id_disciplina": f[2],
                    "data_aula": f[3].isoformat() if f[3] else None,
                    "presente": f[4],
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@frequencias_bp.route("/frequencias", methods=["POST"])
def cadastrar_frequencia():
    """
    Cadastra uma nova frequência.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Frequencia (id_aluno, id_disciplina, data_aula, presente) VALUES (%s, %s, %s, %s)",
            (
                data["id_aluno"],
                data["id_disciplina"],
                data["data_aula"],
                data["presente"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Frequência cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@frequencias_bp.route("/frequencias/<int:id_frequencia>", methods=["PUT"])
def alterar_frequencia(id_frequencia):
    """
    Atualiza os dados de uma frequência existente.
    """
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Frequencia SET id_aluno = %s, id_disciplina = %s, data_aula = %s, presente = %s WHERE id_frequencia = %s",
            (
                data["id_aluno"],
                data["id_disciplina"],
                data["data_aula"],
                data["presente"],
                id_frequencia,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da frequência atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@frequencias_bp.route("/frequencias/<int:id_frequencia>", methods=["DELETE"])
def excluir_frequencia(id_frequencia):
    """
    Exclui uma frequência existente.
    """
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Frequencia WHERE id_frequencia = %s", (id_frequencia,)
        )
        conn.commit()
        return jsonify({"message": "Frequência excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
