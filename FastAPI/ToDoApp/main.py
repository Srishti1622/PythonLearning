from fastapi import FastAPI, Depends
# importing models.py file
import models
from models import Todos
# import engine which we have created in database.py file
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
models.Base.metadata.create_all(bind=engine)

# If sqlite3 is installed then we make use of terminal to manipulate database 
# it will open sqlite environment
# -- sqlite3 database_name.db here sqlite3 todos.db
# it will show the schema of the table
# -- .schema
# run sql queries to manipulate the table
# -- insert into todos (title,description,priority,complete) values ('go to store', 'pick the eggs', 5, False)
# to display the columns/table in terminal in better format use 
# -- .mode column, .mode markdown, .mmode box

# yield means only the code prior to and including the yield statement is executed before sending a response
# the code following the yield statement is exceuted after the response has been delivered
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency injection just means in programming that we need to do something before we execute what we're trying to execute which will allow us to be able to do some kind of code behind the scenes and then inject the dependencies that that function relies on
# here this function relies on our DB opening up, we want to create a session and being able to then return that information back to us and then closing the session behind the scenes
@app.get('/')
def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()