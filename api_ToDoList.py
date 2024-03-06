from flask import Flask, jsonify, abort, request
from datetime import datetime

app = Flask(__name__)

tasks = []
BASE_URL = '/api/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List!'
  
@app.route(BASE_URL + 'tasks', methods=['POST'])
def create_tasks():
    if not request.json:
        abort(404, error='Missing body in request')   
    
    this_time = datetime.now()
    print(request.json)
    
    #Validación para que si no hay nombre o category salga un error
    if not (request.json['name'] or not (request.json['category'])):
        print("ERROR")
        return jsonify({'Error': "Hazlo bien :V"}), 400
    
    task = { 
        'id': len(tasks) + 1 , 
        'name': request.json['name'],
        'catagory': request.json['category'],
        'status': False,
        'created': this_time,
        'update': this_time
    }
    
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    this_task = [task for task in tasks if task[id] == id]
    print('TASK')
    if len(this_task) == 0:
        abort(404, error='ID not found')   
        
    return jsonify({"tasks": this_task[0]})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def check_task(id):
    this_task = [task for task in tasks if task[id] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found')   
        
    print(this_task[0])
    # tasks[this_task[0]['id']]['status'] = True
    this_task[0]['status'] = not this_task[0]['status'] 
    return jsonify({"tasks": this_task[0]})


@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task[id] == id]
    if len(this_task) == 0:
        abort(404, error='ID not found')  
         
    tasks.remove(this_task[0])
    return jsonify({'result': True})


    
if __name__ == "__main__":
    app.run(debug=True)