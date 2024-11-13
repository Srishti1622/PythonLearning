# for testing, we cann't use production db so we need to create a separate fake test db which will be using only for testing purpose

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
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
    # return {'username':'srishtia','id':1, 'role':'user'}

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