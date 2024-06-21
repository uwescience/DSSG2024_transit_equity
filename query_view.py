import os
# import sys

from dotenv import load_dotenv

from sqlalchemy import create_engine, inspect
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.ext.automap import automap_base

load_dotenv()

engine = create_engine(os.getenv('POSTGRES_URL'))

# inspector = inspect(engine)
# schemas = inspector.get_schema_names()

metadata_dssg = MetaData()
metadata_dssg.reflect(bind=engine, views=True, schema='dssg')
Base_dssg = automap_base(metadata=metadata_dssg)
# Base_dssg.prepare(engine, reflect=True, schema='dssg')
Base_dssg.prepare()
print(metadata_dssg.tables.keys())

print(type(Base_dssg.metadata.tables['dssg.v_transactions_apr2023']))
print(type(Base_dssg.metadata.tables['dssg.mv_transactions_apr2023']))

Base_trac = automap_base()
Base_trac.prepare(engine, reflect=True, schema='trac')
print(Base_trac.classes.keys())

