# Reference - https://fastapi.tiangolo.com/tutorial/
# FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
# It uses ASGI (Asynchronous Server Gateway Interface) which is a spiritual successor of WSGI (Web Server Gateway Interface) 

# The key difference between ASGI (Asynchronous Server Gateway Interface) and WSGI (Web Server Gateway Interface) is how they handle requests, specifically synchronous vs. asynchronous requests.

# 1. WSGI (Web Server Gateway Interface)
# Synchronous Interface: WSGI is designed for synchronous applications, meaning that each request is handled one at a time, in a blocking manner. This is the traditional method used by frameworks like Flask and Django.
# Limitations: It is not well-suited for modern real-time web applications that require asynchronous communication, such as WebSockets or background tasks, since each request must wait for the previous one to complete.

# 2. ASGI (Asynchronous Server Gateway Interface)
# Asynchronous Interface: ASGI is designed for both synchronous and asynchronous applications. It supports long-lived connections like WebSockets, making it suitable for modern real-time applications.
# Flexible: ASGI provides greater flexibility by allowing both blocking (synchronous) and non-blocking (asynchronous) code in the same application. Frameworks like FastAPI and newer versions of Django (with Daphne as the ASGI server) support ASGI.
# Better for real-time applications: If you need to handle real-time updates, WebSockets, or background tasks, ASGI is the better choice.

# To run the FastAPI code, we need to run the command-
# uvicorn filename:object(instance name) --reload
# in this case, uvicorn main:app --reload

# It is neccesary to import uvicorn as we will be mentioning that it has to follow ASGI Interface
import uvicorn
from fastapi import FastAPI
# pydantic enforces type hints at runtime, and provides user friendly error when data is invalid
# this is used to get the data from ui in case of post method
# defines how data should be in pure, canonical python and validate it with pydantic
from pydantic import BaseModel

# define a class based on parameters you required from ui
class User(BaseModel):
    name: str
    age: int

# creating an instance of fastAPI
app = FastAPI()

# there is one url as http://localhost:8000/docs
# It will display the complete code in ui for testing our written APIs 
# similar we have /redoc

# Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'messgae':'Hello, API'}

# this url will get from /docs
# url will be like http://locahost:8000/welcome?name=name
@app.get('/welcome')
def welcome(name:str):
    return {'message':f'hello, {name}'}

# provide the dynamic data in the url to hit 
@app.get('/{name}')
def get_name(name:str):
    return {'message':f'hello, {name} getting from /name dynamically'}

# this will be expecting body as it's a post method
@app.post('/posttesting')
def posttesting(user:User):
    user=user.dict()
    name=user['name']
    age=user['age']
    msg="You are a kid bro"
    if age >= 18:
        msg='You are adult now'
    return {'message':msg}

# entry point of code, run the api with uvicorn
# will run on http://127.0.0.1:8000
if __name__=="__main__":
    uvicorn.run(app,host='127.0.0.1',port=800)

# For Deployement in Heroku 

# requirements to deploy the fastapi in heroku 
# gunicorn==19.9.0
# uvloop - dependency of uvicorn
# httptools - dependency of uvicorn
# need to have file named "Procfile" with command - web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
# it's not a text file, need to check for file extention
# here the ccommand description as:
# - web: is specific to Procfile command convention that will help identify the Heroku deployement process to start a web application with the command next to it.
# - gunicorn is the WSGI server to which we are configuring our application to tun, with the following configuration
# - w 4 indicates that we need our application to tun on gunicorn with 4 worker processes
# - k uvicorn.workers.UvicornWorker tells the gunicornto run the application using uvicorn.workers.UvicornWorker worker class
# - main:app is our module main where our FastAPI() app is initialized

