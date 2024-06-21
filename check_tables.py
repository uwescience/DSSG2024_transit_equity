import os
# import sys

from dotenv import load_dotenv

from sqlalchemy import create_engine, inspect
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# from sqlalchemy.sql import text

load_dotenv()

engine = create_engine(os.getenv('POSTGRES_URL'))
# Create an inspector object
inspector = inspect(engine)
# Get the list of table names
schemas = inspector.get_schema_names()
tables = []
for schema in schemas:
    schema_tables = inspector.get_table_names(schema=schema)
    tables.extend([schema+'.'+table for table in schema_tables])
print(tables)
