import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudFrequencias import frequencias_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(frequencias_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudFrequencias.bd.create_connection")
def test_listar_frequencias_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 1, 2, datetime.date(2024, 6, 20), True)]

    response = client.get("/frequencias")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["id_frequencia"] == 1
    assert data[0]["presente"] is True


@patch("app.crudFrequencias.bd.create_connection")
def test_listar_frequencias_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/frequencias")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudFrequencias.bd.create_connection")
def test_buscar_frequencias_por_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 1, 2, datetime.date(2024, 6, 20), True)]

    response = client.get("/frequencias/aluno/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["id_aluno"] == 1


@patch("app.crudFrequencias.bd.create_connection")
def test_buscar_frequencias_por_aluno_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get("/frequencias/aluno/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Nenhuma frequência encontrada para este aluno"


@patch("app.crudFrequencias.bd.create_connection")
def test_buscar_frequencia_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 1, 2, datetime.date(2024, 6, 20), True)

    response = client.get("/frequencias/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id_frequencia"] == 1
    assert data["presente"] is True


@patch("app.crudFrequencias.bd.create_connection")
def test_buscar_frequencia_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get("/frequencias/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Frequência não encontrada"


@patch("app.crudFrequencias.bd.create_connection")
def test_cadastrar_frequencia_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/frequencias",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "data_aula": "2024-06-20",
            "presente": True,
        },
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Frequência cadastrada com sucesso"


@patch("app.crudFrequencias.bd.create_connection")
def test_cadastrar_frequencia_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/frequencias",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "data_aula": "2024-06-20",
            "presente": True,
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudFrequencias.bd.create_connection")
def test_alterar_frequencia_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/frequencias/1",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "data_aula": "2024-06-21",
            "presente": False,
        },
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da frequência atualizados com sucesso"


@patch("app.crudFrequencias.bd.create_connection")
def test_alterar_frequencia_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/frequencias/1",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "data_aula": "2024-06-21",
            "presente": False,
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudFrequencias.bd.create_connection")
def test_excluir_frequencia_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/frequencias/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Frequência excluída com sucesso"


@patch("app.crudFrequencias.bd.create_connection")
def test_excluir_frequencia_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/frequencias/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
