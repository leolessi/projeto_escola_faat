import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.crudAlunos import app


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client


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
            "Endereço Teste",
            "Cidade Teste",
            "Estado Teste",
            "00000-000",
            "País Teste",
            "123456789",
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
            "aluno_id": 1,
            "nome": "Aluno Teste",
            "endereco": "Endereço Teste",
            "cidade": "Cidade Teste",
            "estado": "Estado Teste",
            "cep": "00000-000",
            "pais": "País Teste",
            "telefone": "123456789",
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
            "aluno_id": 1,
            "nome": "Aluno Teste",
            "endereco": "Endereço Teste",
            "cidade": "Cidade Teste",
            "estado": "Estado Teste",
            "cep": "00000-000",
            "pais": "País Teste",
            "telefone": "123456789",
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
            "nome": "Aluno Teste Atualizado",
            "endereco": "Endereço Teste Atualizado",
            "cidade": "Cidade Teste Atualizada",
            "estado": "Estado Teste Atualizado",
            "cep": "00000-000",
            "pais": "País Teste Atualizado",
            "telefone": "987654321",
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
            "nome": "Aluno Teste Atualizado",
            "endereco": "Endereço Teste Atualizado",
            "cidade": "Cidade Teste Atualizada",
            "estado": "Estado Teste Atualizado",
            "cep": "00000-000",
            "pais": "País Teste Atualizado",
            "telefone": "987654321",
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
    assert "Aluno excluído com sucesso".encode("utf-8") in response.data


@patch("app.crudAlunos.bd.create_connection")
def test_excluir_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.delete("/alunos/1")

    assert response.status_code == 500
    assert b"Failed to connect to the database" in response.data
