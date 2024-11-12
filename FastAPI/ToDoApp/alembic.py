# Alembic
# -- lightweight database migration tool for when using sqlalchemy
# -- migration tools allow us to plan, transfer and upgrade resources within databases and to modify our database schema
# -- Alembic allows you to change a sqlalchemy databasetable after it hase been created
# -- currently sqlalchemy will only create new database tables for us, not enhance any but Alembic will allow us to be able to add a column to table within our application without having to delete the existing table 
# -- Alembic provides the creation and invocation of change management scripts
# -- this allows to create migration environments and be able to change data how we like
# -- EX- so we have user table in our database for ToDoApplication, currently which doesn't have phone number column and i want to add contact column so instead of deleting the exsisting user table and then add column, using alembic we can directly add new column in the databse schema

# Alembic commands
# -- alembic init <folder name> : to initializes a new generic environment for our application
# -- alembic revision -m <message> : this will create new revision of the environment, this is where we are going to write all of our database scripts to be able to change and migrate database, this will create a revision ID that will be unique identifier for that databse migration
# -- alembic upgrade <revision#id> : run our upgrade migration to our database like the enhancement for our database
# -- alembic downgrade -1 : this will allow us to downgrade our migration to our database

# After we initialize our project with alembic, two new items will appear in our directory
# -- alembic.ini : file that alembic looks for when invoked, it contains a bunch of configuration information for alembic that we are able to change to match our project
# -- alembic directory : has all environmental properties for alembic, holds all revisions of application, where we can call the migrations for upgrading and downgrading
# These are created automatically by alembic so we can upgrade, downgrade and keep data integrity of our application

Alembic setup
-- pip install alembic
-- then in the terminal itself, run command - alembic init environment_name/folder_name here "alembic init alembic"
