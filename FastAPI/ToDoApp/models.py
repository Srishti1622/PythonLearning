# Models is a way for SQLAlchemy to understand what kind of database tables we are going to create within our database
# Database model is going to be the actual record that is inside a database table

# this the imported from database.py file, the object we have created in that file of the database
from database import Base 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# __tablename__ is just a way for SQLAlchemy to know what to name this table inside our databse
class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))