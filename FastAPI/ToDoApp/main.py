from fastapi import FastAPI
# importing models.py file
import models
# import engine which we have created in database.py file
from database import engine


app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
models.Base.metadata.create_all(bind=engine)