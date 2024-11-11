# Two production database: PostgreSQL, MySQL
# Production DBMS run on their own server and port, which means you need to make sure the database is running, and have authentication linking to the DBMS
# For deployment, we need to deploy the database separate from the application whereas in SQLite3, database deployed along with the application


# PostgreSQL -------------------------------------
# -- production ready RDBMS
# -- open-source relational database management system
# -- secure, requires a server and scalable

# Installing PostgreSQL
# -- go to "https://www.postgresql.org"
# -- click on download, choose window and download the installer with lasted version
# -- open the downloaded .exe file and click on next next until it ask for superadmin password to setup
# -- provide port or leave the default port
# -- then next next and installation will start and then choose this postgresql in stack builder install
# -- once done with all installation, open pg admin app, which is UI for postgresql, provide the password which we set while installing

# Creating tables
# -- if server is not already there click on create server group, else right click on server and then choose register server and provide server name as here "ToDoApplication", host name as "localhost", and password
# -- once you can see the server created, first check for super user called postgres and right click to go to properties and in privileges check for superuser check and is noot present then create one superuser by right clicking on login/group roles
# -- now right click on database, create a new database and provide name as "ToDoApplicationDatabase"
# -- if you are not connected to particular database then right click on that database and choose connect to database
# -- now create tables by running the postgresql queries to create table and add data to those tables

# Connecting the FastAPI with PostgreSQL
# IMPORTANT - everything is same as sqlite3, just change the url as below and engine and then use this setup in ToDoApp/database.py and evrything else keep as it is 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# here 'postgresql://superusername:password@hostname/databasename'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost/ToDoApplicationdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()


# MySQL -------------------------------------------
# -- production ready RDBMS
# -- open-source relational database management system
# -- secure, requires a server and scalable

# Installing MySQL
# -- go to "https://www.mysql.com" and install mysql installer from going to mysql community downloads
# -- open .exe and do next next untill get to setup root password and add new user as username "root" with role DB admin 
# -- uncheck the start the mysql server at system startup
# -- once installed, it will open mysql workbench, double click on local instance and provide the password that we have setted up 

# Creating tables
# -- right click on schemas, and choose create schema and give name as "TodoApplicationDatabase"
# -- now run the mysql queries on the terminal which gets open by clicking on database/schema

# Connecting the FastAPI with MySQL
# IMPORTANT - everything is same as sqlite3, just change the url as below and engine and then use this setup in ToDoApp/database.py and evrything else keep as it is 

