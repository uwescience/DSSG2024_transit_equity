import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy import MetaData, Engine
from sqlalchemy.ext.automap import automap_base, AutomapBase

def get_engine_from_env(path_env: str, postgres_url_key: str = 'POSTGRES_URL') -> Engine:
    '''
    Returns a sqlalchemy Engine object using the environment variables
    Note: This will overwrite the environment variables if they are already set by some other means

    Parameters
    ----------
    path_env : str
        Path to the .env file that contains the environment variables
    postgres_url_key : str
        Key in the .env file that contains the postgres url
    
    Returns
    -------
    Engine
        A sqlalchemy Engine object that is connected to the database
    
    Examples
    --------
    Example 1:
    >>> engine = get_engine_from_env('.env')
    >>> print(type(engine))
    <class 'sqlalchemy.engine.base.Engine'>
    '''
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
    >>> engine = create_engine('postgresql://user:password@localhost:5432/dbname')
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
    engine = get_engine_from_env(path_env)
    print(os.getenv('POSTGRES_URL'))

    SCHEMA = 'orca'
    Base = get_automap_base_with_views(engine=engine, schema=SCHEMA)
    print(type(Base))
    print(Base.classes.keys())