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
st.sidebar.title("Add your task here")

def showTask():
    cursor.execute("select * from todoApp")
    return cursor.fetchall()

def addTask(name,status):
    cursor.execute("insert into todoApp(name,status) values(?,?)",(name,status))
    connection.commit()

def updateTask(task_id,name,status):
    cursor.execute("update todoApp set name=?, status=? where id=?",(name,status,task_id))
    connection.commit()

def deleteTask(task_id):
    cursor.execute("delete from todoApp where id=?",(task_id,))
    connection.commit()

task_name=st.sidebar.text_input("Enter task name here")
task_status=st.sidebar.text_input("Enter task status here")

if st.sidebar.button("Add task"):
    if not task_name:
        st.sidebar.warning("Please enter task name")
    else:
        addTask(task_name,task_status)
        st.sidebar.success("Task added successfully!")

taskList=showTask()
if not taskList:
    st.write("No task to show.")
else:
    st.write("List of task : ")
    for task in taskList:
        col1, col11, col2, col3 = st.columns([4, 4, 2, 2]) 
        with col1:
            st.write(f"**Task Name:** {task[1]}")

        with col11:
            st.write(f"**Task Status:** {task[2]}")

        with col2:
            if st.button("Update",key=f"update_button_{task[0]}"):
                if not task_name:
                    st.sidebar.warning("Please enter task name")
                else:
                    updateTask(task[0],task_name,task_status)
                    st.sidebar.success("Task updated successfully!")

        with col3:
            if st.button("Delete",key=f"delete_button_{task[0]}"):
                deleteTask(task[0])
                st.sidebar.success("Task deleted successfully!")

connection.close()
