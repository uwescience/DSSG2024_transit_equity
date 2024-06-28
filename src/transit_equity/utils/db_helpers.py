import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Engine
from sqlalchemy.ext.automap import automap_base, AutomapBase

def get_engine_from_env(path_env: str, postgres_url_key: str = 'POSTGRES_URL') -> Engine:
    load_dotenv(dotenv_path=path_env)
    engine: Engine = create_engine(os.getenv(postgres_url_key))
    return engine


def get_automap_base_with_views(engine: Engine, schema: str) -> AutomapBase:
    '''
    Returns an AutomapBase object that also provides access to views of a schema

    Parameters
    ----------
    engine : sqlalchemy.Engine
        Engine that is already connected to a database
    schema : str
        Name of schema in the database for which we want to get an AutomapBase object

    Returns
    -------
    AutomapBase
        A declarative automap base for the schema of the database

    Examples
    --------
    Example 1:
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('postgresql://user:password@localhost:5432/dbname'))
    >>> Base = get_automap_base_with_views(engine=engine, schema='orca')
    >>> print(type(Base))
    <class 'sqlalchemy.ext.automap.AutomapBase'>

    Example 2:
    >>> Base = get_automap_base_with_views(engine=get_engine_from_env('.env'), schema='orca')
    >>> print(type(Base))
    <class 'sqlalchemy.ext.automap.AutomapBase'>
    '''
    metadata = MetaData()
    metadata.reflect(bind=engine, views=True, schema=schema)
    Base: AutomapBase = automap_base(metadata=metadata)
    Base.prepare()
    return Base

# Run this from the root to test it
if __name__=='__main__':
    path_env = os.path.join(os.getcwd(), '.env')
    print(path_env)
    load_dotenv(dotenv_path=path_env)
    POSTGRES_URL = 'POSTGRES_URL'
    SCHEMA = 'orca'

    engine = create_engine(os.getenv(POSTGRES_URL))
    Base = get_automap_base_with_views(engine=engine, schema=SCHEMA)
    print(type(Base))
    print(Base.classes.keys())