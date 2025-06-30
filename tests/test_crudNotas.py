import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudNotas import notas_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(notas_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudNotas.bd.create_connection")
def test_listar_notas_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # id_nota, id_aluno, id_disciplina, valor_nota, data_avaliacao
    mock_cursor.fetchall.return_value = [(1, 1, 2, 9.5, datetime.date(2024, 6, 20))]

    response = client.get("/notas")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["valor_nota"] == 9.5


@patch("app.crudNotas.bd.create_connection")
def test_listar_notas_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/notas")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudNotas.bd.create_connection")
def test_buscar_nota_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 1, 2, 9.5, datetime.date(2024, 6, 20))

    response = client.get("/notas/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id_nota"] == 1
    assert data["valor_nota"] == 9.5


@patch("app.crudNotas.bd.create_connection")
def test_buscar_nota_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get("/notas/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Nota não encontrada"


@patch("app.crudNotas.bd.create_connection")
def test_cadastrar_nota_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/notas",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "valor_nota": 8.0,
            "data_avaliacao": "2024-06-21",
        },
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Nota cadastrada com sucesso"


@patch("app.crudNotas.bd.create_connection")
def test_cadastrar_nota_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/notas",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "valor_nota": 8.0,
            "data_avaliacao": "2024-06-21",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudNotas.bd.create_connection")
def test_alterar_nota_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/notas/1",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "valor_nota": 7.5,
            "data_avaliacao": "2024-06-22",
        },
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Dados da nota atualizados com sucesso"


@patch("app.crudNotas.bd.create_connection")
def test_alterar_nota_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/notas/1",
        json={
            "id_aluno": 1,
            "id_disciplina": 2,
            "valor_nota": 7.5,
            "data_avaliacao": "2024-06-22",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudNotas.bd.create_connection")
def test_excluir_nota_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/notas/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Nota excluída com sucesso"


@patch("app.crudNotas.bd.create_connection")
def test_excluir_nota_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/notas/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudNotas.bd.create_connection")
def test_buscar_notas_por_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 1, 2, 9.5, datetime.date(2024, 6, 20)),
        (2, 1, 3, 8.0, datetime.date(2024, 6, 21)),
    ]

    response = client.get("/notas/aluno/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["id_aluno"] == 1


@patch("app.crudNotas.bd.create_connection")
def test_buscar_notas_por_aluno_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get("/notas/aluno/99")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "Nenhuma nota encontrada para este aluno"
