# Alembic
# -- lightweight database migration tool for when using sqlalchemy
# -- migration tools allow us to plan, transfer and upgrade resources within databases and to modify our database schema
# -- Alembic allows you to change a sqlalchemy databasetable after it hase been created
# -- currently sqlalchemy will only create new database tables for us, not enhance any but Alembic will allow us to be able to add a column to table within our application without having to delete the existing table 
# -- Alembic provides the creation and invocation of change management scripts
# -- this allows to create migration environments and be able to change data how we like
# -- EX- so we have user table in our database for ToDoApplication, currently which doesn't have phone number column and i want to add contact column so instead of deleting the exsisting user table and then add column, using alembic we can directly add new column in the databse schema

