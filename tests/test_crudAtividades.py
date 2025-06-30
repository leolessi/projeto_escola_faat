import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudAtividades import atividades_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(atividades_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudAtividades.bd.create_connection")
def test_listar_atividades_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "Passeio ao museu", "2024-07-10")]

    response = client.get("/atividades")
    assert response.status_code == 200
    assert b"Passeio ao museu" in response.data


@patch("app.crudAtividades.bd.create_connection")
def test_listar_atividades_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/atividades")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividades.bd.create_connection")
def test_cadastrar_atividade_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/atividades",
        json={"descricao": "Passeio ao museu", "data_realizacao": "2024-07-10"},
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Atividade cadastrada com sucesso"


@patch("app.crudAtividades.bd.create_connection")
def test_cadastrar_atividade_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/atividades",
        json={"descricao": "Passeio ao museu", "data_realizacao": "2024-07-10"},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividades.bd.create_connection")
def test_alterar_atividade_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/atividades/1",
        json={"descricao": "Passeio ao parque", "data_realizacao": "2024-07-15"},
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da atividade atualizados com sucesso"


@patch("app.crudAtividades.bd.create_connection")
def test_alterar_atividade_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/atividades/1",
        json={"descricao": "Passeio ao parque", "data_realizacao": "2024-07-15"},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividades.bd.create_connection")
def test_excluir_atividade_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/atividades/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Atividade excluída com sucesso"


@patch("app.crudAtividades.bd.create_connection")
def test_excluir_atividade_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/atividades/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
