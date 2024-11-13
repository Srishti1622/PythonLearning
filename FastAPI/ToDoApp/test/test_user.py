from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status
import pytest
from ..models import Todos

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_get_user(test_user):
    response=client.get('/user/get_user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'usertesing'
    assert response.json()['email'] == 'usertesting@gmail.com'
    assert response.json()['first_name'] == 'user'
    assert response.json()['last_name'] == 'testing'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '111111111'

def test_change_password(test_user):
    request_data={
        'password':'usertesing',
        'new_password':'newuser'
    }
    response=client.put('/user/change_password', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_not_found(test_user):
    request_data={
        'password':'wrong',
        'new_password':'newuser'
    }
    response=client.put('/user/change_password', json=request_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Old Password does not matched'}

def test_change_phone_number(test_user):
    response=client.put('/user/change_phone_number/1234567890')
    assert response.status_code == status.HTTP_204_NO_CONTENT