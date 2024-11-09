# IMPORTANT: SQLAlchemy cannot enhance a table for us. It can only create a table for us.
# We can enhance a table using something called Alembic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# this url is going to used to create a location of this database on our fastapi application
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todoApp.db'

# create a database engine that we can use to be able to open up a connection and to able to use our database
# connect arguments are arguments that we can pass into our create engine, which will allow us to define some kind of connection to a database
# by default, SQLite will only allow one thread to communicate with it
# this is to prevent any kind of accident sharing of the same connection for different kind of requests
# but in fastAPI it's very normal to have more than one thread that colud interact with the database at the same time
# so to make sure SQLite knows that we don't want to check the same thread all the time because there colud be multiple threads happening to our SQLite database by mentioning 'check_same_thread=False'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# this is the session local, which we are going to be using in our application, we want to bind to the engine that we created and we want to make sure that our auto commits and auto flushes are false or the database transactions are going to try and do something automatically and we want to be fully control of everything our database will do in the future
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base which is an object of the database which is going to be able to control our database
Base=declarative_base()