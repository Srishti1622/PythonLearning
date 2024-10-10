# Creating a ToDo Application which will use all HTTP Verbs - GET, POST, PUT, DELETE

from flask import Flask, jsonify, redirect, url_for, request

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

@app.route('/addtask',methods=['GET','POST'])
def addtask():
    if request.method=='POST':
        task={
            "task_id":tasks[-1]['task_id']+1 if tasks else 1,
            "task_name":request.json['task_name'],
            "task_status":request.json['task_status']
        }
        tasks.append(task)
        return jsonify(tasks)
    return redirect(url_for('alltasks'))

@app.route('/updatetask/<int:task_id>',methods=['PUT'])
def updatetask(task_id):
    task=[task for task in tasks if task['task_id']==task_id]
    if not task:
        return jsonify({"error":'no task found with given id'})
    task[0]['task_name']=request.json['task_name']
    task[0]['task_status']=request.json['task_status']
    return jsonify(tasks)

@app.route('/deletetask/<int:task_id>',methods=['DELETE'])
def deletetask(task_id):
    global tasks
    task=[task for task in tasks if task['task_id']==task_id]
    if not task:
        return jsonify({"error":'no task found with given id'})
    tasks=[task for task in tasks if task['task_id']!=task_id]
    return jsonify(tasks)
    

if __name__=="__main__":
    app.run(debug=True)