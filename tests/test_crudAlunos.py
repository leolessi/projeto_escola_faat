import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.crudAlunos import alunos_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(alunos_bp)
    app.testing = True
    return app.test_client()


@patch("app.crudAlunos.bd.create_connection")
def test_listar_alunos_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (
            1,
            "Aluno Teste",
            "2010-05-10",
            1,
            "Responsável Teste",
            "11999999999",
            "responsavel@email.com",
            "Nenhuma",
        )
    ]

    response = client.get("/alunos")
    assert response.status_code == 200
    assert b"Aluno Teste" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_listar_alunos_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.get("/alunos")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_cadastrar_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post(
        "/alunos",
        json={
            "nome_completo": "Aluno Teste",
            "data_nascimento": "2010-05-10",
            "id_turma": 1,
            "nome_responsavel": "Responsável Teste",
            "telefone_responsavel": "11999999999",
            "email_responsavel": "responsavel@email.com",
            "informacoes_adicionais": "Nenhuma",
        },
    )

    assert response.status_code == 201
    assert b"Aluno cadastrado com sucesso" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_cadastrar_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post(
        "/alunos",
        json={
            "nome_completo": "Aluno Teste",
            "data_nascimento": "2010-05-10",
            "id_turma": 1,
            "nome_responsavel": "Responsável Teste",
            "telefone_responsavel": "11999999999",
            "email_responsavel": "responsavel@email.com",
            "informacoes_adicionais": "Nenhuma",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_alterar_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.put(
        "/alunos/1",
        json={
            "nome_completo": "Aluno Teste Atualizado",
            "data_nascimento": "2010-05-10",
            "id_turma": 1,
            "nome_responsavel": "Responsável Atualizado",
            "telefone_responsavel": "987654321",
            "email_responsavel": "responsavel_atualizado@email.com",
            "informacoes_adicionais": "Atualizado",
        },
    )

    assert response.status_code == 200
    assert b"Dados do aluno atualizados com sucesso" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_alterar_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.put(
        "/alunos/1",
        json={
            "nome_completo": "Aluno Teste Atualizado",
            "data_nascimento": "2010-05-10",
            "id_turma": 1,
            "nome_responsavel": "Responsável Atualizado",
            "telefone_responsavel": "987654321",
            "email_responsavel": "responsavel_atualizado@email.com",
            "informacoes_adicionais": "Atualizado",
        },
    )

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_excluir_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.delete("/alunos/1")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Aluno excluído com sucesso"


@patch("app.crudAlunos.bd.create_connection")
def test_excluir_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/alunos/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
