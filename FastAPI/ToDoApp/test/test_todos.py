# for testing, we cann't use production db so we need to create a separate fake test db which will be using only for testing purpose

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///.testdb.db"

engine=create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread':False},
    poolclass=StaticPool
)

TestingSessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# this function is overriding the get_db() in todos.py when we are doing testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# mocking the data for user dependency
def override_get_current_user():
    return {'username':'srishtia','id':1, 'role':'admin'}

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

client=TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='todo for testing',
        description='mocking data',
        priority=4,
        complete=False,
        owner_id=1
    )
    db=TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

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
    response=client.get('/todo')
    assert response.status_code == status.HTTP_201_CREATED