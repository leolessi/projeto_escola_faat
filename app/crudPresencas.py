from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/presencas", methods=["GET"])
def listar_presencas():
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


@app.route("/presencas", methods=["POST"])
def cadastrar_presenca():
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


@app.route("/presencas/<int:id_presenca>", methods=["PUT"])
def alterar_presenca(id_presenca):
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


@app.route("/presencas/<int:id_presenca>", methods=["DELETE"])
def excluir_presenca(id_presenca):
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
