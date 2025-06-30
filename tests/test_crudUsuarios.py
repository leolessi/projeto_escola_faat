import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudUsuarios import usuarios_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(usuarios_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudUsuarios.bd.create_connection")
def test_listar_usuarios_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, "admin", "123456", "admin", 1)]

    response = client.get("/usuarios")
    assert response.status_code == 200
    assert b"admin" in response.data


@patch("app.crudUsuarios.bd.create_connection")
def test_listar_usuarios_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/usuarios")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudUsuarios.bd.create_connection")
def test_buscar_usuario_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, "admin", "123456", "admin", 1)

    response = client.get("/usuarios/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["login"] == "admin"


@patch("app.crudUsuarios.bd.create_connection")
def test_buscar_usuario_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get("/usuarios/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Usuário não encontrado"


@patch("app.crudUsuarios.bd.create_connection")
def test_cadastrar_usuario_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/usuarios",
        json={
            "login": "admin",
            "senha": "123456",
            "nivel_acesso": "admin",
            "id_professor": 1,
        },
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Usuário cadastrado com sucesso"


@patch("app.crudUsuarios.bd.create_connection")
def test_cadastrar_usuario_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/usuarios",
        json={
            "login": "admin",
            "senha": "123456",
            "nivel_acesso": "admin",
            "id_professor": 1,
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudUsuarios.bd.create_connection")
def test_alterar_usuario_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/usuarios/1",
        json={
            "login": "admin",
            "senha": "nova_senha",
            "nivel_acesso": "admin",
            "id_professor": 1,
        },
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados do usuário atualizados com sucesso"


@patch("app.crudUsuarios.bd.create_connection")
def test_alterar_usuario_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/usuarios/1",
        json={
            "login": "admin",
            "senha": "nova_senha",
            "nivel_acesso": "admin",
            "id_professor": 1,
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudUsuarios.bd.create_connection")
def test_excluir_usuario_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/usuarios/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Usuário excluído com sucesso"


@patch("app.crudUsuarios.bd.create_connection")
def test_excluir_usuario_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/usuarios/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
