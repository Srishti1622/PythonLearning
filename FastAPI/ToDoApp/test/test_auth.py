from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db]=override_get_db

def test_authenticate_user(test_user):
    db=TestingSessionLocal()

    valid_user=authenticate_user(test_user.username,'usertesing', db)
    assert valid_user is not None
    assert valid_user.username==test_user.username

    invalid_user=authenticate_user('wrong', 'usertesing', db)
    assert invalid_user is False

    wrongpassword=authenticate_user(test_user.username, 'wrong', db)
    assert wrongpassword is False

def test_create_access_token(test_user):
    username='testuser'
    user_id=1
    role='user'
    expire_delta=timedelta(days=1)

    token=create_access_token(username, user_id, role, expire_delta)

    decoded_token=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature':False})

    assert decoded_token['sub']==username
    assert decoded_token['id']==user_id
    assert decoded_token['role']==role

# @pytest.mark.asyncio
# async def test_get_current_user(test_user):
def test_get_current_user(test_user):
    encode={'sub':'testuser','id':1, 'role':'admin'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    # user=await get_current_user(token=token)
    user=get_current_user(token=token)
    assert user=={'username':'testuser','id':1,'role':'admin'}

# @pytest.mark.asyncio
# async def test_get_current_user(test_user):
def test_get_current_user_invalid_token(test_user):
    encode={'role':'user'}
    token=jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        # await get_current_user(token=token)
        get_current_user(token=token)

    assert excinfo.value.status_code==401
    assert excinfo.value.detail=='Could not validate the user'

