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

def test_listar_tarefas():

    response = requests.get(f"{BASE_URL}/tarefas")
    assert response.status_code == 200

    response_json = response.json()
    assert 'tarefas' in response_json
    assert 'total_tarefas' in response_json

    assert 'id' in response_json['tarefas'][0]
    assert 'nome' in response_json['tarefas'][0]
    assert 'descricao' in response_json['tarefas'][0]
    assert 'completada' in response_json['tarefas'][0]

def test_visualizar_tarefa():

    tarefa_id = tarefas[0].get('id')
    response = requests.get(f"{BASE_URL}/tarefas/{tarefa_id}")
    assert response.status_code == 200

    response_json = response.json()
    assert 'id' in response_json
    assert 'nome' in response_json
    assert 'descricao' in response_json
    assert 'completada' in response_json

    assert uuid.UUID(str(response_json.get('id')))

    assert response_json.get('id') in tarefa_id
    assert response_json.get('nome') in tarefas[0].get('nome')
    assert response_json.get('descricao') in tarefas[0].get('descricao')
    assert response_json.get('completada') == bool(tarefas[0].get('completada'))

def test_atualizar_tarefa():

    tarefa_atualizada = {
        'nome': 'Tarefa python',
        'descricao': 'Descrição da tarefa python',
        'completada': True
    }

    tarefa_id = tarefas[0].get('id')
    response = requests.put(f"{BASE_URL}/tarefas/{tarefa_id}", json=tarefa_atualizada)
    assert response.status_code == 204

    response = requests.get(f"{BASE_URL}/tarefas/{tarefa_id}")
    assert response.status_code == 200

    response_json = response.json()
    assert 'id' in response_json
    assert 'nome' in response_json
    assert 'descricao' in response_json
    assert 'completada' in response_json

    assert uuid.UUID(str(response_json.get('id')))

    assert tarefa_atualizada.get('nome') == response_json.get('nome')
    assert tarefa_atualizada.get('descricao') == response_json.get('descricao')
    assert tarefa_atualizada.get('completada') == response_json.get('completada')

def test_remover_tarefa():

    tarefa_id = tarefas[0].get('id')
    response = requests.delete(f"{BASE_URL}/tarefas/{tarefa_id}")
    assert response.status_code == 204

    response = requests.get(f"{BASE_URL}/tarefas/{tarefa_id}")
    assert response.status_code == 404