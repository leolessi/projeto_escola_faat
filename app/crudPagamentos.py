from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/pagamentos", methods=["GET"])
def listar_pagamentos():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Pagamento")
        pagamentos = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_pagamento": pagamento[0],
                        "id_aluno": pagamento[1],
                        "data_pagamento": pagamento[2],
                        "valor_pago": float(pagamento[3]),
                        "forma_pagamento": pagamento[4],
                        "referencia": pagamento[5],
                        "status": pagamento[6],
                    }
                    for pagamento in pagamentos
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/pagamentos", methods=["POST"])
def cadastrar_pagamento():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Pagamento (id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                data["id_aluno"],
                data["data_pagamento"],
                data["valor_pago"],
                data["forma_pagamento"],
                data["referencia"],
                data["status"],
            ),
        )
        conn.commit()
        return jsonify({"message": "Pagamento cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/pagamentos/<int:id_pagamento>", methods=["PUT"])
def alterar_pagamento(id_pagamento):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Pagamento
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, forma_pagamento = %s, referencia = %s, status = %s
            WHERE id_pagamento = %s
            """,
            (
                data["id_aluno"],
                data["data_pagamento"],
                data["valor_pago"],
                data["forma_pagamento"],
                data["referencia"],
                data["status"],
                id_pagamento,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados do pagamento atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/pagamentos/<int:id_pagamento>", methods=["DELETE"])
def excluir_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        return jsonify({"message": "Pagamento excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
