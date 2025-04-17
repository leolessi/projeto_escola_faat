from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/atividade_aluno", methods=["GET"])
def listar_atividade_aluno():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade_Aluno")
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


@app.route("/atividade_aluno", methods=["POST"])
def cadastrar_atividade_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Atividade_Aluno (id_atividade, id_aluno)
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


@app.route("/atividade_aluno/<int:id_atividade>/<int:id_aluno>", methods=["DELETE"])
def excluir_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Atividade_Aluno WHERE id_atividade = %s AND id_aluno = %s",
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
