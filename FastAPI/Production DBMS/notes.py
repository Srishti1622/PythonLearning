# Production DBMS run on their own server and port, which means you need to make sure the database is running, and have authentication linking to the DBMS
# For deployment, we need to deploy the database separate from the application whereas in SQLite3, database deployed along with the application


# PostgreSQL 
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
-- if server is not already there click on create server group, else right click on server and then choose register server and provide server name as here "ToDoApplication", host name as "localhost", and password
-- once you can see the server created, first check for super user called postgres and right click to go to properties and in privileges check for superuser check and is noot present then create one superuser by right clicking on login/group roles
-- now right click on database, create a new database and provide name as "ToDoApplicationDatabase"
-- if you are not connected to particular database then right click on that database and choose connect to database
-- now create tables by running the postgresql queries to create table and add data to those tables

