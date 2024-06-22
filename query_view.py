import os
# import sys

from dotenv import load_dotenv

from sqlalchemy import create_engine, inspect, func
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.ext.automap import automap_base, AutomapBase

load_dotenv()

engine = create_engine(os.getenv('POSTGRES_URL'))

# inspector = inspect(engine)
# schemas = inspector.get_schema_names()

metadata_dssg = MetaData()
metadata_dssg.reflect(bind=engine, views=True, schema='dssg')
Base_dssg: AutomapBase = automap_base(metadata=metadata_dssg)
# Base_dssg.prepare(engine, reflect=True, schema='dssg')
Base_dssg.prepare()
print(metadata_dssg.tables.keys())

# print(type(Base_dssg.metadata.tables['dssg.v_transactions_apr2023']))
# print(type(Base_dssg.metadata.tables['dssg.mv_transactions_apr2023']))
mv_transactions = Base_dssg.metadata.tables['dssg.mv_transactions_apr2023']

Base_trac: AutomapBase = automap_base()
Base_trac.prepare(engine, reflect=True, schema='trac')

agencies = Base_trac.metadata.tables['trac.agencies']
# agencies = Base_trac.classes.agencies

# print(Base_trac.classes.keys())

print(type(mv_transactions))
# print(mv_transactions.columns)
print(type(agencies))
# print(agencies.columns)
# print(type(Base_trac.classes.agencies))

Session = sessionmaker(bind=engine)

# # Create a session
session = Session()
# Join query example
# stmt = select(func.count(agencies.c.orca_agency_id).label('Agency Count'))
stmt = select(mv_transactions.c.txn_id).join(agencies, mv_transactions.c.source_agency_id == agencies.c.orca_agency_id)\
.limit(10)
print(stmt)
results = session.execute(statement=stmt)
# # results = session.query(agencies).all()
for row in results:
    print(row)

session.close()