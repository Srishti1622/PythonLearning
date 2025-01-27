from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
# importing models.py file
# from models import Todos        # normal path
from ..models import Todos        # relative path
# import engine which we have created in database.py file
# from database import engine, SessionLocal       # normal path
from ..database import engine, SessionLocal       # relative path
from typing import Annotated
from sqlalchemy.orm import Session
# import to inject dependency for user authentication
from .auth import get_current_user


router=APIRouter()

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

# whenever we include this dependency then, first always it will check for authentication and in swagger ui, will get it show as a lock/unlock icon to login/logout
user_dependency = Annotated[dict, Depends(get_current_user)]

class ToDoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

# querying tabble named 'Todos'
# @router.get('/', status_code=status.HTTP_200_OK)
# def read_all_todos(db: db_dependency):
#     return db.query(Todos).all()
@router.get('/', status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed!')
    
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()

# @router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
# def read_specific_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail='Todo not found')
@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
def read_specific_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed!')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')

# @router.post('/todo', status_code=status.HTTP_201_CREATED)
# def create_todo(db: db_dependency, todo: ToDoRequest):
#     todo_model = Todos(**todo.dict())
#     db.add(todo_model)
#     db.commit()
# with user authentication
@router.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo: ToDoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed!')
    todo_model = Todos(**todo.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()

# @router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
# def update_specific_todo(db: db_dependency, todo: ToDoRequest, todo_id: int = Path(gt=0)):
#     todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found')
    
#     todo_model.title=todo.title
#     todo_model.description=todo.description
#     todo_model.priority=todo.priority
#     todo_model.complete=todo.complete

#     db.add(todo_model)
#     db.commit()
@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_specific_todo(user: user_dependency, db: db_dependency, todo: ToDoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed!')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()

# @router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_specific_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model=db.query(Todos).filter(Todos.id==todo_id).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail='Todo not found')

#     db.query(Todos).filter(Todos.id==todo_id).delete()
#     db.commit()
@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed!')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()