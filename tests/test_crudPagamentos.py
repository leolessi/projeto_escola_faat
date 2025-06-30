import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudPagamentos import pagamentos_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(pagamentos_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudPagamentos.bd.create_connection")
def test_listar_pagamentos_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            1,  # id_pagamento
            1,  # id_aluno
            "2024-06-25",  # data_pagamento
            500.00,  # valor_pago
            "boleto",  # forma_pagamento
            "junho/2024",  # referencia
            "pago",  # status
        )
    ]

    response = client.get("/pagamentos")
    assert response.status_code == 200
    assert b"junho/2024" in response.data


@patch("app.crudPagamentos.bd.create_connection")
def test_listar_pagamentos_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/pagamentos")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPagamentos.bd.create_connection")
def test_cadastrar_pagamento_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/pagamentos",
        json={
            "id_aluno": 1,
            "data_pagamento": "2024-06-25",
            "valor_pago": 500.00,
            "forma_pagamento": "boleto",
            "referencia": "junho/2024",
            "status": "pago",
        },
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Pagamento cadastrado com sucesso"


@patch("app.crudPagamentos.bd.create_connection")
def test_cadastrar_pagamento_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/pagamentos",
        json={
            "id_aluno": 1,
            "data_pagamento": "2024-06-25",
            "valor_pago": 500.00,
            "forma_pagamento": "boleto",
            "referencia": "junho/2024",
            "status": "pago",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPagamentos.bd.create_connection")
def test_alterar_pagamento_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/pagamentos/1",
        json={
            "id_aluno": 1,
            "data_pagamento": "2024-06-26",
            "valor_pago": 550.00,
            "forma_pagamento": "cartao",
            "referencia": "junho/2024",
            "status": "pago",
        },
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados do pagamento atualizados com sucesso"


@patch("app.crudPagamentos.bd.create_connection")
def test_alterar_pagamento_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/pagamentos/1",
        json={
            "id_aluno": 1,
            "data_pagamento": "2024-06-26",
            "valor_pago": 550.00,
            "forma_pagamento": "cartao",
            "referencia": "junho/2024",
            "status": "pago",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPagamentos.bd.create_connection")
def test_excluir_pagamento_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/pagamentos/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Pagamento excluído com sucesso"


@patch("app.crudPagamentos.bd.create_connection")
def test_excluir_pagamento_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/pagamentos/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
