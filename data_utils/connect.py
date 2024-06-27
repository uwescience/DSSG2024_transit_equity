from sqlalchemy import MetaData, Engine
from sqlalchemy.ext.automap import automap_base, AutomapBase


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
    >>> from sqlalchemy import create_engine
    >>> engine_main = create_engine('postgresql://user:password@localhost:5432/dbname'))
    >>> Base = get_automap_base_with_views(engine=engine_main, schema='orca')
    >>> print(type(Base))
    <class 'sqlalchemy.ext.automap.AutomapBase'>
    '''
    metadata = MetaData()
    metadata.reflect(bind=engine, views=True, schema=schema)
    Base: AutomapBase = automap_base(metadata=metadata)
    Base.prepare()
    return Base

if __name__=='__main__':
    import os

    from dotenv import load_dotenv
    from sqlalchemy import create_engine

    path_env = os.path.join(os.path.dirname(os.getcwd()), '.env')
    load_dotenv(dotenv_path=path_env)
    POSTGRES_URL = 'POSTGRES_URL'
    SCHEMA = 'orca'

    engine_main = create_engine(os.getenv(POSTGRES_URL))
    Base = get_automap_base_with_views(engine=engine_main, schema=SCHEMA)
    print(type(Base))
    print(Base.classes.keys())