from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/atividades", methods=["GET"])
def listar_atividades():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Atividade")
        atividades = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_atividade": atividade[0],
                        "descricao": atividade[1],
                        "data_realizacao": atividade[2],
                    }
                    for atividade in atividades
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividades", methods=["POST"])
def cadastrar_atividade():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Atividade (descricao, data_realizacao)
            VALUES (%s, %s)
            """,
            (
                data["descricao"],
                data["data_realizacao"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Atividade cadastrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividades/<int:id_atividade>", methods=["PUT"])
def alterar_atividade(id_atividade):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Atividade
            SET descricao = %s, data_realizacao = %s
            WHERE id_atividade = %s
            """,
            (
                data["descricao"],
                data["data_realizacao"],
                id_atividade,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados da atividade atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/atividades/<int:id_atividade>", methods=["DELETE"])
def excluir_atividade(id_atividade):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Atividade WHERE id_atividade = %s", (id_atividade,))
        conn.commit()
        return jsonify({"message": "Atividade excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
