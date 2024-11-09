from fastapi import APIRouter
from pydantic import BaseModel
from models import Users

# it's a route instead of entire application which will be using in main.py file
router=APIRouter()

# not added id and is_active as id is auto-increament and is_active as initial created user will stay active
class UserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

@router.get('/auth')
def get_user():
    return {"user":"authenticated"}

@router.post('/user')
def create_user(user: UserRequest):
    user_model=Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=user.password,
        role=user.role,
        is_active=True
    )
    return user_model
    # db.add(user_model)
    # db.commit()