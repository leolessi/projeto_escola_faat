import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudAtividadeAluno import atividade_aluno_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(atividade_aluno_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_listar_atividade_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [(1, 2)]

    response = client.get("/atividade_aluno")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data[0]["id_atividade"] == 1
    assert data[0]["id_aluno"] == 2


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_listar_atividade_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/atividade_aluno")
    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_cadastrar_atividade_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/atividade_aluno",
        json={"id_atividade": 1, "id_aluno": 2},
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Atividade associada ao aluno com sucesso"


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_cadastrar_atividade_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/atividade_aluno",
        json={"id_atividade": 1, "id_aluno": 2},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_atualizar_atividade_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/atividade_aluno/1/2",
        json={"novo_id_atividade": 3, "novo_id_aluno": 4},
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert (
        data["message"] == "Associação entre atividade e aluno atualizada com sucesso"
    )


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_atualizar_atividade_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/atividade_aluno/1/2",
        json={"novo_id_atividade": 3, "novo_id_aluno": 4},
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_excluir_atividade_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/atividade_aluno/1/2")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Associação entre atividade e aluno excluída com sucesso"


@patch("app.crudAtividadeAluno.bd.create_connection")
def test_excluir_atividade_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/atividade_aluno/1/2")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
