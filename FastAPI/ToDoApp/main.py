from fastapi import FastAPI
# importing models.py file
# import models      # normal path
from .models import Base      # realtive path
# import engine which we have created in database.py file
# from database import engine, SessionLocal       # normal path
from .database import engine, SessionLocal      # realtive path
# import auth from auth.py file 
# from routers import auth, todos, admin, user       # normal path
from .routers import auth, todos, admin, user      # realtive path

# IMPORTANT NOTE:  as now we have changed all the paths to relative paths, so to run the application we need to run the command - uvicorn ToDoApp.main:app --reload

app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
# models.Base.metadata.create_all(bind=engine)        # normal path
Base.metadata.create_all(bind=engine)       # relative path

# this is specially for production, to check does the connection working and returning status code 200 
@app.get('/healthy')
def health_check():
    return {'status':'Healthy'}

# to let application know to include the mentioned routers route in the application
# if more than one router present then include all in each new line
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)