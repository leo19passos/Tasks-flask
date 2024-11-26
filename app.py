from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)
tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data['description'])
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"mensagem": "nova tarefa criada com sucesso!" })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    output = {
                "tasks": tasks_list,
                "total_tasks": len(tasks)
                }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task (id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

        return jsonify({"mensagem":"não foi encontrado!"}),404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task (id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if task == None:
        return jsonify({"mensagem": "não foi possivel encontrar a atividade!"}), 404

    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.completed = data['completed']

    return jsonify({"mensagem": "Tarefa atualizada com sucesso!"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t

    if not task:
        return jsonify({"mensagem": "Não foi possivel encontar a atividade!"}), 404

    tasks.remove(task)
    return jsonify({"mensagem": "Tarefa deletada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)