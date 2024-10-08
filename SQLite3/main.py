# Reference: https://docs.python.org/3/library/sqlite3.html

# In Python3, SQLite3 get installed automatically we just need to import it.

import sqlite3

# connect to an SQLite database
# connect() is and inbuilt function which will take database name to create a connection to given database, create only if it does not exist
connection=sqlite3.connect('learning.db')
print("Connection created!")

# create a cursor object to iterate over all the rows and do manipulation
# will use this cursor object to execute all queries
cursor=connection.cursor()
print("cursor object created!")

# creating a table
cursor.execute('''
    create table if not exists Employees(
        id integer primary key,
        name text not null,
        age integer,
        department text
    )
''')
print("Table created!")

# Insert the data in the table
cursor.execute('''
    insert into Employees(name,age,department) values("Srishti",23,"CSE")
''')
print("One data inserted!")

moreDataToInsert=[
    ('Akshay',24,'CSE'),
    ('Jatin',26,'CSE'),
    ('Tina',28,'EE'),
    ('Akshat',24,'CSE'),
    ('Puru',24,'ME'),
]

# to insert multiple data in one go
cursor.executemany('''
    insert into Employees(name,age,department) values(?,?,?)
''',moreDataToInsert)
print("Multiple data inserted in one go!")

# Read or Query the data from table
cursor.execute('''
    select * from Employees
''')
print("Queried table!")

# fetchall() is a function to get all the records from select command
rows=cursor.fetchall()
print("Stored data inside table ----")
for row in rows:
    print(row)

# Update the existing data in the table
cursor.execute('''
    update Employees set age=30 where name='Tina'
''')
print("Updated table data!")

cursor.execute('''
    select * from Employees
''')
print("Again quering the table after updating the records!")

rows=cursor.fetchall()
print("Stored data ----")
for row in rows:
    print(row)

# Delete data from the table
cursor.execute('''
    delete from Employees where name='Tina'
''')
cursor.execute('''
    select * from Employees
''')
print("Again quering the table after deleting the records!")

rows=cursor.fetchall()
print("Stored data ----")
for row in rows:
    print(row)

# commit the changes always after executing any query -- important
connection.commit()
print("All changes commited!")
# close the connection at last, once the connection is closed you will not able to perform any opertaion on the database -- important
connection.close()
print("Connection closed!")