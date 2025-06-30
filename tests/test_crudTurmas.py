import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudTurmas import turmas_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(turmas_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudTurmas.bd.create_connection")
def test_listar_turmas_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "Turma A", 1, "08:00-12:00")]

    response = client.get("/turmas")
    assert response.status_code == 200
    assert b"Turma A" in response.data


@patch("app.crudTurmas.bd.create_connection")
def test_listar_turmas_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/turmas")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudTurmas.bd.create_connection")
def test_cadastrar_turma_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/turmas",
        json={"nome_turma": "Turma A", "id_professor": 1, "horario": "08:00-12:00"},
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Turma cadastrada com sucesso"


@patch("app.crudTurmas.bd.create_connection")
def test_cadastrar_turma_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/turmas",
        json={"nome_turma": "Turma A", "id_professor": 1, "horario": "08:00-12:00"},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudTurmas.bd.create_connection")
def test_alterar_turma_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/turmas/1",
        json={
            "nome_turma": "Turma A - Atualizada",
            "id_professor": 1,
            "horario": "13:00-17:00",
        },
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da turma atualizados com sucesso"


@patch("app.crudTurmas.bd.create_connection")
def test_alterar_turma_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/turmas/1",
        json={
            "nome_turma": "Turma A - Atualizada",
            "id_professor": 1,
            "horario": "13:00-17:00",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudTurmas.bd.create_connection")
def test_excluir_turma_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/turmas/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Turma excluída com sucesso"


@patch("app.crudTurmas.bd.create_connection")
def test_excluir_turma_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/turmas/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database"
