# for testing, we cann't use production db so we need to create a separate fake test db which will be using only for testing purpose
from .utils import *
from ..routers.todos import get_db, get_current_user
from fastapi import status
import pytest
from ..models import Todos

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_read_all_todos(test_todo):
    response=client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title':'todo for testing',
        'description':'mocking data',
        'priority':4,
        'id':1,
        'complete':False,
        'owner_id':1}]

def test_read_specific_todo(test_todo):
    response=client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'title':'todo for testing',
        'description':'mocking data',
        'priority':4,
        'id':1,
        'complete':False,
        'owner_id':1}

def test_read_specific_todo_not_found(test_todo):
    response=client.get('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo not found'}

def test_create_todo(test_todo):
    request_data={
        'title':'new todo',
        'description':'new todo',
        'priority':4,
        'complete':False
    }
    response=client.post('/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db=TestingSessionLocal()
    # id ==2 as id=1 is created by fixture 
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    assert model.priority==request_data.get('priority')
    assert model.complete==request_data.get('complete')

def test_update_specific_todo(test_todo):
    request_data={
        'title':'updated new todo',
        'description':'updated new todo',
        'priority':4,
        'complete':False,
    }
    response=client.put('/todo/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    assert model.priority==request_data.get('priority')
    assert model.complete==request_data.get('complete')

def test_update_specific_todo_not_found(test_todo):
    request_data={
        'title':'updated new todo',
        'description':'updated new todo',
        'priority':4,
        'complete':False,
    }
    response=client.put('/todo/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo not found'}

def test_delete_specific_todo(test_todo):
    response=client.delete('/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db=TestingSessionLocal() 
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None

def test_delete_specific_todo_not_found(test_todo):
    response=client.delete('/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail':'Todo not found'}