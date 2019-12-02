## Python/flask/MySQL Service for tasks 
##
##  Purpose: provide restful web api for tasks 
##
##  Author : Simon Li  Nov 2019
##

# https://code.visualstudio.com/Docs/editor/debugging
###############################################################
# Use package flask   (pip install flask)
from flask import Flask, jsonify

from flask import abort, make_response
from flask import request
from flask import url_for

###############################################################
app = Flask(__name__)
print("app: %s" % app)

###############################################################
# Database service
from MySQLService import MySQLService
mysql = MySQLService()
mysql.table = "tasks"  

##############################################################
# add url
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        #else:
        #    new_task[field] = task[field]
        new_task[field] = task[field]
    return new_task

# curl -i http://localhost:5000/todo/api/v1.0/tasks
#print("api endpoint: %s" % "http://localhost:5000/todo/api/v1.0/tasks");

#############################################################
# Error: error handler, 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#############################################################
# Api - Dummy   
@app.route('/', methods=['GET'])
def get_dummy():
    return "Welcome Rest API from python/MySQL"

#############################################################
# Api 1: R[get], get full tasks   
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in mysql.tasks()]})

#############################################################
# Api 2: R[get], get a list per id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    taskSel = [task for task in mysql.tasks() if task['id'] == task_id]
    if len(taskSel) == 0:
        abort(404)
    return jsonify({'task': taskSel[0]})


#############################################################
# Api 3: C[post], creat e task
# Windows: curl -i -H "Content-Type: application/json" -X POST -d "{"""title""":"""Read a book"""}" http://localhost:5000/todo/api/v1.0/tasks
# Unix: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.p0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': mysql.tasks()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    
    # Persistence - insert
    mysql.add((task["id"], task["title"], task["description"], task["done"]))

    return jsonify({'task': task}), 201

#############################################################
# Api 4: U[put], update a task
# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/todo/api/v1.0/tasks/2
# curl -i -H "Content-Type: application/json" -X PUT -d "{"""done""":true}' http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    taskSel = [task for task in mysql.tasks() if task['id'] == task_id]
    if len(taskSel) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    taskSel[0]['title'] = request.json.get('title', taskSel[0]['title'])
    taskSel[0]['description'] = request.json.get('description', taskSel[0]['description'])
    taskSel[0]['done'] = request.json.get('done', taskSel[0]['done'])
    
    # Persistence - update
    valueSet = [
            {"field": 'title',       "value": taskSel[0]['title']},
            {"field": 'description', "value": taskSel[0]['description']},
            {"field": 'done',        "value": taskSel[0]['done']}
    ]
    mysql.update("id = %d" % (taskSel[0]['id']), valueSet)
    
    return jsonify({'task': taskSel[0]})


#############################################################
# Api 5: D[delete], delete task
# curl -i -H "Content-Type: application/json" -X DELETE -d http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    taskSel = [task for task in mysql.tasks() if task['id'] == task_id]
    if len(taskSel) == 0:
        abort(404)
    
    # Persistence - delete
    mysql.remove("id = %d" % (taskSel[0]['id']))

    return jsonify({'result': True})

#############################################################
if __name__ == '__main__':
    app.run(debug=True)
