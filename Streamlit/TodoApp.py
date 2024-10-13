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

def addTask(name,status):
    cursor.execute("insert into todoApp(name,status) values(?,?)",(name,status))

def updateTask():
    cursor.execute("update todoApp set ")

task_name=st.text_input("Enter task name here",key="")
task_status=st.text_input("Enter task status here")

if st.button("Add task"):
    if task_name:
