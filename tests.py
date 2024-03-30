import pytest
import requests
import uuid

BASE_URL = 'http://127.0.0.1:5000'
tarefas = []

def test_criar_tarefa():
    tarefa = {
        'nome': 'Nova Tarefa',
        'descricao': 'Descrição da tarefa'
    }

    response = requests.post(f"{BASE_URL}/tarefas", json=tarefa)
    assert response.status_code == 201

    response_json = response.json()
    tarefas.append(response_json.get('data'))
    assert 'mensagem' in response_json
    assert 'data' in response_json
    
    data = response_json.get('data')
    assert 'id' in data
    assert 'nome' in data
    assert 'descricao' in data
    assert 'completada' in data

    assert uuid.UUID(str(data.get('id')))
    assert tarefa.get('nome') == data.get('nome')
    assert tarefa.get('descricao') == data.get('descricao')
    assert False == data.get('completada')