# Reference - https://fastapi.tiangolo.com/tutorial/
# FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
# Important: fastAPI looks in a chronological order from top to bottom to see what matches the URL so, try to write the function and endpoints by small to large urls, specially in case of path parameters

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
# here --reload means when we make any change to our fastapi code it will automaticaally detect the changes and restart the server
# Also there is another way to run fastapi app as-
# fastapi run filename.py  -- to run at production level mode
# fastapi dev filename-py -- to run at development level mode

# It is neccesary to import uvicorn as we will be mentioning that it has to follow ASGI Interface
import uvicorn
from fastapi import FastAPI, Body, Path, Query
# pydantic enforces type hints at runtime, and provides user friendly error when data is invalid
# this is used to get the data from ui in case of post method
# defines how data should be in pure, canonical python and validate it with pydantic
# FastAPI is now compatible with both Pydantic v1 and Pydantic v2.
# Based on how new the version of FastAPI you are using, there could be small method name changes.
# The three biggest are:
# 1- .dict() function is now renamed to .model_dump()
# 2- schema_extra function within a Config class is now renamed to json_schema_extra
# 3- Optional variables need a =None example: id: Optional[int] = None
from pydantic import BaseModel, Field
from typing import Optional
# to make class with whatever data is avaiable, it will provide inbuild data validation
from enum import Enum

# define a class based on parameters you required from ui
class User(BaseModel):
    name: str
    age: int = Field(gt=0)

# model_config is used to create more descriptive request example within our swagger docus
    model_config={
        "json_schema_extra":{
            "example":{
                "name":"Srishti",
                "age": 24
            }
        }
    }

# define a class based on whatever we want to make user see
class AvaiableFood(str ,Enum):
    indian='indian'
    american='american'
    italian='italian'

fooditems={
    'indian':['Samosa','Dosa'],
    'american':['hot dog','apple pie'],
    'italian':['ravioli','pizza']
}

# creating an instance of fastAPI
app = FastAPI()

# there is one url as http://localhost:8000/docs
# It will display the complete code in ui for testing our written APIs 
# similar we have /redoc
# this is what called as "Swagger UI"

# Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'messgae':'Hello, API'}

# this url will get from /docs
# url will be like http://locahost:8000/welcome?name=name
@app.get('/welcome')
def welcome(name:str):
    return {'message':f'hello, {name}'}

# path paramters: provide the dynamic data in the url to hit 
# %20 means space in dynamic urls
# keep in mind that order matters with path parameters as if "/books/{dynamic_params}" comes first and then "/books/mybook", so 2nd endpoint will never get executed as it will consider mybook as dynamic params and always go to 1st endpoint
@app.get('/{name}')
def get_name(name:str = Path(min_length=5)):
    return {'message':f'hello, {name} getting from /name dynamically'}

# query parameters: are request parameters that have been attached after "?" and have name=value pair as
# /books/?category=maths
# query parameters are sort and filter through data that is not marked by a path parameter
@app.get('/query/')
def query_parameter(testing: int = Query(gt=4)):
    if testing>10:
        return {'message':'testing is greater than 10'}
    return {'message':'testing is under 10'}

# this will be expecting body as it's a post method
@app.post('/posttesting')
def posttesting(user:User):
    user=user.dict() 
    # if .dict() not work then use .model_dump()
    # user=User(**user.dict())
    # print(type(user))
    name=user['name']
    age=user['age']
    msg="You are a kid bro"
    if age >= 18:
        msg='You are adult now'
    return {'message':msg}

# case to test enum
# as here we are using this enum, we don't need to explixity apply validation to check is the user provided food name is present or not 
@app.get('/getitems/{foodname}')
def getitems(foodname: AvaiableFood):
    return {'msg':f'you selected {foodname}','fooditems':fooditems.get(foodname)}

class Items(BaseModel):
    id: Optional[int] = Field(title="id is not needed") # pydantic v1
    # id: Optional[int] = None # pydantic v2
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0,lt=6)

items=[
    {'name':'one','category':'one'},
    {'name':'two','category':'two'},
    {'name':'three','category':'three'},
    {'name':'four','category':'four'},
]
@app.post('/additems')
def additems(food=Body()):
    items.append(food)
    return items

# put method also have body to whatever data we want to update
@app.put('/updateitems')
def updateitems(food=Body()):
    for i in range(len(items)):
        print(items[i])
        if items[i].get('name').casefold()==food.get('name').casefold():
            items[i]=food
    return items

@app.delete('/deleteitems/{name}')
def deleteitems(name: str):
    for i in range(len(items)):
        if items[i].get('name').casefold()==name.casefold():
            items.pop(i)
            break
    return items

# entry point of code, run the api with uvicorn
# will run on http://127.0.0.1:8000
if __name__=="__main__":
    uvicorn.run(app,host='127.0.0.1',port=8000)

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

# Status Codes
# An HTTP Status Code is used to help the Client(the user or system submitting data to the server) to understand what happened on the server side application
# -- 1xx -> Information Response: Request Processing
# -- 2xx -> Success: Request Successfully complete
# -- 3xx -> Redirection: Further action must be complete
# -- 4xx -> Client Errors: An error was caused by the client
# -- 5xx -> Server Errors: An error occurred on the server

# 2xx Successful Status Codes:
# -- 200: OK -> Standard response for a Successful request. commonly used for Successful GET requests when data is being returned
# -- 201: Created -> The request has been Successful, creating a new resource. Used when a POST creates an entity
# -- 204: No Content -> The request has been Successful, did not create an entity nor return anything. Commonly used with PUt requests

# 4xx Successful Status Codes:
# -- 200: Bad Request -> Cannot process request due to client error. Commonly used for invalid request methods
# -- 401: Unauthorized -> Client does not have valid authentication for target resource
# -- 404: Not Found -> The clients requested resource can not be found 
# -- 422: Unprocessable Entity -> Semantic Errors in Client Request

# 5xx Successful Status Codes:
# -- 500: Internal Server Error -> Generic Error Message, when an unexpected issue on the server happened