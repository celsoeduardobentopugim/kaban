from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

 
tasks = [
    {'id': 1, 'title': 'Task 1', 'status': 'To Do'},
    {'id': 2, 'title': 'Task 2', 'status': 'In Progress'},
    {'id': 3, 'title': 'Task 3', 'status': 'Done'}
]

class TaskListResource(Resource):
    def get(self):
        return jsonify(tasks)
    
    def post(self):
        new_task = request.get_json()
        new_task['id'] = len(tasks) + 1  
        tasks.append(new_task)
        return jsonify(new_task), 201  

class TaskResource(Resource):
    def get(self, task_id):
        task = next((task for task in tasks if task['id'] == task_id), None)
        if task is None:
            return {'message': 'Task not found'}, 404
        return jsonify(task)
    
    def put(self, task_id):
        task = next((task for task in tasks if task['id'] == task_id), None)
        if task is None:
            return {'message': 'Task not found'}, 404
        
        data = request.get_json()
        task['title'] = data.get('title', task['title'])
        task['status'] = data.get('status', task['status'])
        return jsonify(task)
    
    def delete(self, task_id):
        global tasks
        tasks = [task for task in tasks if task['id'] != task_id]
        return '', 204  


api.add_resource(TaskListResource, '/tasks') 
api.add_resource(TaskResource, '/tasks/<int:task_id>')  

if __name__ == '__main__':
    app.run(debug=True)
