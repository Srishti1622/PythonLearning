from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
# special form that will be sight;y more secure than fastapi form, using this will be able to see the form in swagger ui itself
from fastapi.security import OAuth2PasswordRequestForm

# it's a route instead of entire application which will be using in main.py file
router=APIRouter()

# for hashed password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
formData = Annotated[OAuth2PasswordRequestForm, Depends()]

def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

# not added id and is_active as id is auto-increament and is_active as initial created user will stay active
class UserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.get('/auth')
def get_user(db: db_dependency):
    return db.query(Users).all()

@router.post('/signup', status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user: UserRequest):
    user_model=Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        role=user.role,
        is_active=True
    )
    
    db.add(user_model)
    db.commit()

@router.post('/authcheck')
def login_for_access_token(form: formData, db: db_dependency):
    if not authenticate_user(form.username,form.password,db):
        raise HTTPException(status_code=404,detail='Either user does not exists or invalid password')
    return 'user authenticated successful'