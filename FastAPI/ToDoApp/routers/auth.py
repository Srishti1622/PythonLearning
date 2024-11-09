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


# JSON Web Token (https://jwt.io/)
# -- It is a self-contained way to securely transmit data and information between two parties using JSON object
# -- It can be trusted because each JWT can be digitally signed, which in return allows the server to know if the JWT has been changed at all
# -- JWT should be used when dealing with authentication
# -- JWT is a great way for information to be exchanged between the server and client

# JSON Web Token Structure
# -- It is created of three separate parts separated by dots(.) which includes 'aaaaaaaa.bbbbbbbb.cccccccc' where header:(a), payload:(b), signature:(c)
# -- A JWT header usually consist of two parts which then encoded using Base64 to create the first part of the JWT(a): 
#     {
#         "alg": "HS256", # the algorithm for signing
#         "typ": "JWT" # the specific type of token
#     }
# -- A JWT Payload consists of the data. The payloads data contains claims, and there are three different types of claims and is then encoded using Base64 to create the second part of the JWT(b): 
#     -- Registered(predefined, recommended but not mandatory) -- top three registered claims incluse ISS(stands for issuer, this claim identifies the principal that issued the JWT), sub(stands for subject and holds statements about the subject. The subject value must be scoped either locallly or globally unique. Think of a subject as an ID for the JWT) and exp(stands for expiration time, which is when the JWT expries. This claim makes sure that the current date and time is before the expiration date and time of the token. It is not mandatory but extremely useful. One thing you never want to do is have your token never expire. this is because if your token never expires, then anyone who has a JWT will be authorized by the server)
#     -- Public
#     -- Private
#     {
#         "sub": "1234567890",
#         "name": "srishti",
#         "given_name": "srishti",
#         "family_name": "agrawal",
#         "email": "jssjj@gmail.com",
#         "admin": true
#     }
# -- A JWT signature is created by using the algorithm in the header to hash out the encoded header, encoded payload with a secret. The secret can be anything, but is saved somewhere on the server that the client does not have access to and is the third and final part of the JWT(c)
#     HMACSA256(
#         base64UrlEncode(header) + "." +
#         base64UrlEncode(payload),
#         secretkey)     secretkey may be any string like learnonline

# When working with a JWT, the requester usually sends a token in the authorization header using the bearer schema