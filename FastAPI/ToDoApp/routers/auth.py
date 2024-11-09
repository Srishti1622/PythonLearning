from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status

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

@router.post('/token')
def login_for_access_token():
    return 'token'