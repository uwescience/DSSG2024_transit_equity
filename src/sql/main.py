import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
from sqlalchemy.sql import text

engine = create_engine("postgresql://u_himanshu@10.142.198.170:5432/orca")

# Create an inspector object
inspector = inspect(engine)

# Get the list of table names
tables = inspector.get_table_names()

# Print the list of tables
# print("Tables in the database:")
# for table in tables:
#     print(table)

with engine.connect() as con:

    statement = text("""SELECT *
    FROM pg_catalog.pg_tables
     WHERE schemaname != 'pg_catalog' AND 
     schemaname != 'information_schema';""")

    rs = con.execute(statement)
    for row in rs:
        print(row)