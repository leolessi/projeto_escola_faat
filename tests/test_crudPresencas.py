import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudPresencas import presencas_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(presencas_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudPresencas.bd.create_connection")
def test_listar_presencas_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 1, "2024-06-26", True)]

    response = client.get("/presencas")
    assert response.status_code == 200
    assert b"2024-06-26" in response.data


@patch("app.crudPresencas.bd.create_connection")
def test_listar_presencas_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/presencas")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPresencas.bd.create_connection")
def test_cadastrar_presenca_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/presencas",
        json={"id_aluno": 1, "data_presenca": "2024-06-26", "presente": True},
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Presença cadastrada com sucesso"


@patch("app.crudPresencas.bd.create_connection")
def test_cadastrar_presenca_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/presencas",
        json={"id_aluno": 1, "data_presenca": "2024-06-26", "presente": True},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPresencas.bd.create_connection")
def test_alterar_presenca_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/presencas/1",
        json={"id_aluno": 1, "data_presenca": "2024-06-27", "presente": False},
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da presença atualizados com sucesso"


@patch("app.crudPresencas.bd.create_connection")
def test_alterar_presenca_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/presencas/1",
        json={"id_aluno": 1, "data_presenca": "2024-06-27", "presente": False},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudPresencas.bd.create_connection")
def test_excluir_presenca_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/presencas/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Presença excluída com sucesso"


@patch("app.crudPresencas.bd.create_connection")
def test_excluir_presenca_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/presencas/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database"
