import os
# import sys

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session

load_dotenv()

engine = create_engine(os.getenv('POSTGRES_URL'))

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

agencies = Table('agencies', Base.metadata, schema='trac', autoload_with=engine)
print(type(agencies))
print(agencies.columns)

stmt = select(agencies).where(agencies.columns.orca_agency_id == 2)

session = Session(engine)
results = session.execute(statement=stmt)
for row in results:
    print(row)

session.close()
