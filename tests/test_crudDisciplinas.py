import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudDisciplinas import disciplinas_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(disciplinas_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudDisciplinas.bd.create_connection")
def test_listar_disciplinas_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "Matemática", 1)]

    response = client.get("/disciplinas")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["nome_disciplina"] == "Matemática"


@patch("app.crudDisciplinas.bd.create_connection")
def test_listar_disciplinas_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/disciplinas")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudDisciplinas.bd.create_connection")
def test_buscar_disciplina_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, "Matemática", 1)

    response = client.get("/disciplinas/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["nome_disciplina"] == "Matemática"


@patch("app.crudDisciplinas.bd.create_connection")
def test_buscar_disciplina_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get("/disciplinas/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Disciplina não encontrada"


@patch("app.crudDisciplinas.bd.create_connection")
def test_cadastrar_disciplina_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/disciplinas",
        json={"nome_disciplina": "Matemática", "id_professor": 1},
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Disciplina cadastrada com sucesso"


@patch("app.crudDisciplinas.bd.create_connection")
def test_cadastrar_disciplina_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/disciplinas",
        json={"nome_disciplina": "Matemática", "id_professor": 1},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudDisciplinas.bd.create_connection")
def test_alterar_disciplina_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/disciplinas/1",
        json={"nome_disciplina": "Matemática Avançada", "id_professor": 1},
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da disciplina atualizados com sucesso"


@patch("app.crudDisciplinas.bd.create_connection")
def test_alterar_disciplina_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/disciplinas/1",
        json={"nome_disciplina": "Matemática Avançada", "id_professor": 1},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudDisciplinas.bd.create_connection")
def test_excluir_disciplina_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/disciplinas/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Disciplina excluída com sucesso"


@patch("app.crudDisciplinas.bd.create_connection")
def test_excluir_disciplina_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/disciplinas/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
