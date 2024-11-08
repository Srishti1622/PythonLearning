from sqlalchemy import create_engine

# this url is going to used to create a location of this database on our fastapi application
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

# create a database engine that we can use to be able to open up a connection and to able to use our database
# connect arguments are arguments that we can pass into our create engine, which will allow us to define some kind of connection to a database
# by default, SQLite will only allow one thread to communicate with it
# this is to prevent any kind of accident sharing of the same connection for different kind of requests
# but in fastAPI it's very normal to have more than one thread that colud interact with the database at the same time
# so to make sure SQLite knows that we don't want to check the same thread all the time because there colud be multiple threads happening to our SQLite database by mentioning 'check_same_thread=False'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})