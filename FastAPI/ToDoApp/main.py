from fastapi import FastAPI
# importing models.py file
import models
# import engine which we have created in database.py file
from database import engine, SessionLocal
# import auth from auth.py file 
from routers import auth, todos, admin


app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
models.Base.metadata.create_all(bind=engine)

# to let application know to include the mentioned routers route in the application
# if more than one router present then include all in each new line
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)