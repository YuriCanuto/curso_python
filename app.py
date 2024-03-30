from flask import Flask, request, jsonify
from models.tarefas import Tarefa
import uuid

app = Flask(__name__)

tarefas = []

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.get_json()
    tarefa = Tarefa(uuid.uuid4(), nome=data.get('nome'), descricao=data.get('descricao'))
    tarefas.append(tarefa)
    return jsonify({
        'mensagem': 'Nova tarefa cadastrada',
        'data': tarefa.to_dict()
        }), 201

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    response = {
        "tarefas": [tarefa.to_dict() for tarefa in tarefas ],
        "total_tarefas": len(tarefas)
    }
    return jsonify(response)

@app.route('/tarefas/<string:id>', methods=['GET'])
def visualizar_tarefa(id):
    for tarefa in tarefas:
        if str(tarefa.id) == id:
            return jsonify(tarefa.to_dict())
    return jsonify({"mensagem": "Tarefa não encontada"}), 404

@app.route('/tarefas/<string:id>', methods=['PUT'])
def atualizar_tarefa(id):
    for tarefa in tarefas:
        if str(tarefa.id) == id:
            data =  request.get_json()

            tarefa.nome = data.get('nome')
            tarefa.descricao = data.get('descricao')
            tarefa.completada = data.get('completada')
        
            return jsonify({"mensagem": "Tarefa atualizada"}), 204

    return jsonify({"mensagem": "Tarefa não encontada"}), 404

@app.route('/tarefas/<string:id>', methods=['DELETE'])
def deletar_tarefa(id):
    for tarefa in tarefas:
        if str(tarefa.id) == id:
            tarefas.remove(tarefa)
            return jsonify({"mensagem": "Tarefa removida"})
    
    return jsonify({"mensagem": "Tarefa não encontada"}), 404
        
if __name__ == "__main__":
    app.run(debug=True)