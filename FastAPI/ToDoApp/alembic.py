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

# Alembic setup
# -- pip install alembic
# -- then in the terminal itself, run command - alembic init environment_name/folder_name here "alembic init alembic"
# -- change the sqlalchemy.url path n alembic.ini file to our database file url
# --then go to alembic/env.py file and import models and then remove if statement which line sets up loggers basically and make the lines inside that if statement as normal without if
# -- then setup target_metadata=models.Base.metadata in alembic/env.py
# -- now create new revision by running command - alembic revision -m "create phone number for user table"
# -- it will create new revision_id.py file inside alembic/version/filename.py
# -- go to revision file and modify the upgrade function as 
#     def upgrade() -> None:
#         op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
# -- then run command to upgrade - alembic upgrade revision_id
# -- also need to add the column in models.py file where defined the schema for tables
# -- go to revision file and modify the downgrade function as 
#     def downgrade() -> None:
#         op.drop_column('users', 'phone_number')
# -- then run command to downgrade - alembic downgrade -1
# -- also need to remove the column in models.py file where defined the schema for tables
