# Creating a ToDo Application which will use all HTTP Verbs - GET, POST, PUT, DELETE

from flask import Flask, jsonify

app=Flask(__name__)

tasks=[
    {'task_id':1,'task_name':'learning','task_status':'in progress'},
    {'task_id':2,'task_name':'learning2','task_status':'in progress2'}
]

@app.route('/alltasks',methods=['GET'])
def alltasks():
    if not tasks:
        return jsonify({'error':'task list is empty'})
    return jsonify(tasks)

@app.route('/alltasks/<int:task_id>')
def specifictask(task_id):
    task=[task for task in tasks if task['task_id']==task_id]
    if not task:
        return jsonify({"error":'no task found with given id'})
    return jsonify(task)


if __name__=="__main__":
    app.run(debug=True)