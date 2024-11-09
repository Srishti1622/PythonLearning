from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
# importing models.py file
import models
from models import Todos
# import engine which we have created in database.py file
from database import engine, SessionLocal
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