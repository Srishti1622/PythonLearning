from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
# importing models.py file
# from models import Todos        # normal path
from ..models import Todos        # realtive path
# import engine which we have created in database.py file
# from database import engine, SessionLocal     # normal path
from ..database import engine, SessionLocal       # relative path
from typing import Annotated
from sqlalchemy.orm import Session
# import to inject dependency for user authentication
from .auth import get_current_user


router=APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).all()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_specific_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401, detail='Authentication failed!')
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()