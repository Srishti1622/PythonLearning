# creating code to connect with sqlite3 db

import sqlite3

# connect to sqlite
connection=sqlite3.connect("student.db")

# create a cusore object for manipulating the db
cursor=connection.cursor()

# query to create the table
table_info="""
create table STUDENT( 
    NAME VARCHAR(25), 
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT 
)
"""

# execute the query
cursor.execute(table_info)