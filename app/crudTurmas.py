from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/turmas", methods=["GET"])
def listar_turmas():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Turma")
        turmas = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_turma": turma[0],
                        "nome_turma": turma[1],
                        "id_professor": turma[2],
                        "horario": turma[3],
                    }
                    for turma in turmas
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/turmas", methods=["POST"])
def cadastrar_turma():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Turma (nome_turma, id_professor, horario)
            VALUES (%s, %s, %s)
            """,
            (
                data["nome_turma"],
                data.get("id_professor"),
                data["horario"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Turma cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/turmas/<int:id_turma>", methods=["PUT"])
def alterar_turma(id_turma):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Turma
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s
            """,
            (
                data["nome_turma"],
                data.get("id_professor"),
                data["horario"],
                id_turma,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da turma atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/turmas/<int:id_turma>", methods=["DELETE"])
def excluir_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Turma WHERE id_turma = %s", (id_turma,))
        conn.commit()
        return jsonify({"message": "Turma excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
