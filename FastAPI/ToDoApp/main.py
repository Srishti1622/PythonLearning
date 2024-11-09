from fastapi import FastAPI
# importing models.py file
import models
# import engine which we have created in database.py file
from database import engine


app=FastAPI()

# this will create a database in this mentioned location in database.py in the variable SQLALCHEMY_DATABASE_URL
# in this case it's inside ToDoApp foldera
models.Base.metadata.create_all(bind=engine)



# If sqlite3 is installed then we make use of terminal to manipulate database 
# it will open sqlite environment
# -- sqlite3 database_name.db here sqlite3 todos.db
# it will show the schema of the table
# -- .schema
# run sql queries to manipulate the table
# -- insert into todos (title,description,priority,complete) values ('go to store', 'pick the eggs', 5, False)
# to display the columns/table in terminal in better format use 
# -- .mode column, .mode markdown, .mmode box