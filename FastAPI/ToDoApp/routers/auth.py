from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
# from models import Users        # normal path
from ..models import Users        # relative path
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
# from database import SessionLocal       # normal path
from ..database import SessionLocal       # relative path
from starlette import status
from datetime import timedelta, datetime, timezone
# special form that will be sight;y more secure than fastapi form, using this will be able to see the form in swagger ui itself
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

# it's a route instead of entire application which will be using in main.py file
router=APIRouter(
    prefix='/auth',  # each endpoint start with prefix
    tags=['auth']
)

SECRET_KEY = '5db3199bb9475825b11125df1c6ee82ed4d0ba64b51458eed702e5d81286e855'
ALGORITHM = 'HS256'
# SECRET_KEY = '5db3199bb9475825b11125df1c6ee82ed4d0ba64b51458eed702e5d81286e855ex-29whnes98d23snd92ed3j'
# ALGORITHM = 'HS256ex-123450'
# SECRET_KEY = ''
# ALGORITHM = ''

# for hashed password
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# tokenUrl parameter conatins the url that the client will send to our fastapi application
# basically the endpoint in which we are getting username and password from user and returning the access token
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

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
    return user

def create_access_token(username: str, user_id: int,
role:str, expire_delta: timedelta):
    encode = {
        'sub':username,
        'id':user_id,
        'role': role
    }
    expires=datetime.now(timezone.utc) + expire_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate the user')
        return{'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate the user')

# not added id and is_active as id is auto-increament and is_active as initial created user will stay active
class UserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    # remove phone_number from here also after doing downgrade
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.get('/user')
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
        is_active=True,
        # remove phone_number from here also after doing downgrade
        phone_number=user.phone_number
    )
    
    db.add(user_model)
    db.commit()

@router.post('/login', response_model=Token)
def login_for_access_token(form: formData, db: db_dependency):
    user = authenticate_user(form.username,form.password,db)
    if not user:
        raise HTTPException(status_code=401,detail='Either user does not exists or invalid password')
    
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token, 'token_type': 'bearer'}


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