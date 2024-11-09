from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
# importing models.py file
import models
from models import Todos
# import engine which we have created in database.py file
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
# import auth from auth.py file 
from routers import auth


app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
models.Base.metadata.create_all(bind=engine)

# to let application know to include the mentioned routers route in the application
app.include_router(auth.router)

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
db_dependency = Annotated[Session, Depends(get_db)]

class ToDoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get('/', status_code=status.HTTP_200_OK)
def read_all_todos(db: db_dependency):
    return db.query(Todos).all()

@app.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_specific_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

@app.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo: ToDoRequest):
    todo_model = Todos(**todo.dict())
    db.add(todo_model)
    db.commit()

@app.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_specific_todo(db: db_dependency, todo: ToDoRequest, todo_id: int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()

@app.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()