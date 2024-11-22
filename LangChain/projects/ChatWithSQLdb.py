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

# insert the data in student table
cursor.execute("""Insert into STUDENT values('Srishti','Full stack ai engineer','A',100)""")
cursor.execute("""Insert into STUDENT values('Akshay','Full stack ai engineer','A',95)""")
cursor.execute("""Insert into STUDENT values('Krishna','ai engineer','B',45)""")
cursor.execute("""Insert into STUDENT values('Mansi','software engineer','A',78)""")
cursor.execute("""Insert into STUDENT values('John','ai engineer','B',67)""")
cursor.execute("""Insert into STUDENT values('Jatin','software engineer','B',34)""")

# display all the records
print("The inserted records are:")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

# at last we always have to commit and close the connection
connection.commit()
connection.close()


# connecting with MySQL
# first we need to download the mysql database and wrokbench
# then we need to create table and add records in that table