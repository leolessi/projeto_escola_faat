from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/professores", methods=["GET"])
def listar_professores():
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


@app.route("/professores", methods=["POST"])
def cadastrar_professor():
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


@app.route("/professores/<int:id_professor>", methods=["PUT"])
def alterar_professor(id_professor):
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


@app.route("/professores/<int:id_professor>", methods=["DELETE"])
def excluir_professor(id_professor):
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
