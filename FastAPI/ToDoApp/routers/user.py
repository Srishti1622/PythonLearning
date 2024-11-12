from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
# importing models.py file
import models
from models import Users
# import engine which we have created in database.py file
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
# import to inject dependency for user authentication
from .auth import get_current_user, bcrypt_context


router=APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/get_user', status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
def change_password(user: user_dependency, db: db_dependency, new_user: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    if not bcrypt_context.verify(new_user.password,user_model.hashed_password):
        raise HTTPException(status_code=404, detail='Old Password does not matched')
    user_model.hashed_password=bcrypt_context.hash(new_user.new_password)
    db.add(user_model)
    db.commit() 

@router.put('/change_phone_number/{number}', status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(user: user_dependency, db: db_dependency, number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model=db.query(Users).filter(Users.id==user.get('id')).first()
    user_model.phone_number=number
    db.add(user_model)
    db.commit() 
    