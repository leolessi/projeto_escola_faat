import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudProfessores import professores_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(professores_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudProfessores.bd.create_connection")
def test_listar_professores_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, "Professor Teste", "professor@email.com", "11999999999")
    ]

    response = client.get("/professores")
    assert response.status_code == 200
    assert b"Professor Teste" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_listar_professores_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/professores")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_cadastrar_professor_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/professores",
        json={
            "nome_completo": "Professor Teste",
            "email": "professor@email.com",
            "telefone": "11999999999",
        },
    )

    assert response.status_code == 201
    assert b"Professor cadastrado com sucesso" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_cadastrar_professor_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/professores",
        json={
            "nome_completo": "Professor Teste",
            "email": "professor@email.com",
            "telefone": "11999999999",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_alterar_professor_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/professores/1",
        json={
            "nome_completo": "Professor Atualizado",
            "email": "prof_atualizado@email.com",
            "telefone": "11988887777",
        },
    )

    assert response.status_code == 200
    assert b"Dados do professor atualizados com sucesso" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_alterar_professor_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/professores/1",
        json={
            "nome_completo": "Professor Atualizado",
            "email": "prof_atualizado@email.com",
            "telefone": "11988887777",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudProfessores.bd.create_connection")
def test_excluir_professor_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/professores/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Professor excluído com sucesso"


@patch("app.crudProfessores.bd.create_connection")
def test_excluir_professor_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/professores/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
