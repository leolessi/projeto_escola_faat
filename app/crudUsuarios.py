from flask import Flask, request, jsonify
import Util.bd as bd

app = Flask(__name__)


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Usuario")
        usuarios = cursor.fetchall()
        return (
            jsonify(
                [
                    {
                        "id_usuario": usuario[0],
                        "login": usuario[1],
                        "senha": usuario[2],
                        "nivel_acesso": usuario[3],
                        "id_professor": usuario[4],
                    }
                    for usuario in usuarios
                ]
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Usuario (login, senha, nivel_acesso, id_professor)
            VALUES (%s, %s, %s, %s)
            """,
            (
                data["login"],
                data["senha"],
                data["nivel_acesso"],
                data.get("id_professor"),
            ),
        )
        conn.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/usuarios/<int:id_usuario>", methods=["PUT"])
def alterar_usuario(id_usuario):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Usuario
            SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s
            WHERE id_usuario = %s
            """,
            (
                data["login"],
                data["senha"],
                data["nivel_acesso"],
                data.get("id_professor"),
                id_usuario,
            ),
        )
        conn.commit()
        return jsonify({"message": "Dados do usuário atualizados com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def excluir_usuario(id_usuario):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Usuario WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007, debug=True)
