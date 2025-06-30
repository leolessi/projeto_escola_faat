from flask import request, jsonify, Blueprint
from Util import bd
import logging

logger = logging.getLogger(__name__)
pagamentos_bp = Blueprint("pagamentos", __name__)


@pagamentos_bp.route("/pagamentos", methods=["GET"])
def listar_pagamentos():
    """
    Lista todos os pagamentos cadastrados.
    ---
    tags:
      - Pagamentos
    responses:
      200:
        description: Lista de pagamentos retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_pagamento:
                type: integer
              id_aluno:
                type: integer
              data_pagamento:
                type: string
                format: date
              valor_pago:
                type: number
                format: float
              forma_pagamento:
                type: string
              referencia:
                type: string
              status:
                type: string
      400:
        description: Erro ao buscar os pagamentos.
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


@pagamentos_bp.route("/pagamentos", methods=["POST"])
def cadastrar_pagamento():
    """
    Cadastra um novo pagamento.
    ---
    tags:
      - Pagamentos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_pagamento:
              type: string
              format: date
            valor_pago:
              type: number
              format: float
            forma_pagamento:
              type: string
            referencia:
              type: string
            status:
              type: string
    responses:
      201:
        description: Pagamento cadastrado com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao cadastrar o pagamento.
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


@pagamentos_bp.route("/pagamentos/<int:id_pagamento>", methods=["PUT"])
def alterar_pagamento(id_pagamento):
    """
    Atualiza os dados de um pagamento existente.
    ---
    tags:
      - Pagamentos
    parameters:
      - name: id_pagamento
        in: path
        required: true
        type: integer
        description: ID do pagamento a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_pagamento:
              type: string
              format: date
            valor_pago:
              type: number
              format: float
            forma_pagamento:
              type: string
            referencia:
              type: string
            status:
              type: string
    responses:
      200:
        description: Dados do pagamento atualizados com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao atualizar os dados do pagamento.
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


@pagamentos_bp.route("/pagamentos/<int:id_pagamento>", methods=["DELETE"])
def excluir_pagamento(id_pagamento):
    """
    Exclui um pagamento existente.
    ---
    tags:
      - Pagamentos
    parameters:
      - name: id_pagamento
        in: path
        required: true
        type: integer
        description: ID do pagamento a ser excluído.
    responses:
      200:
        description: Pagamento excluído com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Erro ao excluir o pagamento.
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
        cursor.execute("DELETE FROM Pagamento WHERE id_pagamento = %s", (id_pagamento,))
        conn.commit()
        return jsonify({"message": "Pagamento excluído com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
