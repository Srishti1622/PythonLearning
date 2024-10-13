import streamlit as st
import sqlite3

connection=sqlite3.connect("todoapp.db")
cursor=connection.cursor()

cursor.execute("""
    create table if not exists todoApp(
        id integer primary key autoincrement,
        name text not null,
        status text
    ) 
""")
connection.commit()

st.title("To-Do-App")

def showTask():
    cursor.execute("select * from todoApp")
    return cursor.fetchall()

def addTask(name,status):
    cursor.execute("insert into todoApp(name,status) values(?,?)",(name,status))
    task=showTask()
    for t in task:
        print(t)
    connection.commit()

def updateTask():
    cursor.execute("update todoApp set ")

task_name=st.text_input("Enter task name here")
task_status=st.text_input("Enter task status here")

if st.button("Add task"):
    if not task_name:
        st.warning("Please enter task name")
    else:
        addTask(task_name,task_status)
        st.success("Task added successfully!")

print("show list yrr")
if st.button("Show task list"):
    taskList=showTask()
    for task in taskList:
        print(task)
