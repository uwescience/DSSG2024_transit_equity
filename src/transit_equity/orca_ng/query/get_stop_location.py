import datetime

from sqlalchemy import Table, Select
from sqlalchemy.ext.automap import AutomapBase

from . import get_schema_key
from ..schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA
from ..schema_tables import DSSG_SCHEMA_TABLES, ORCA_SCHEMA_TABLES, TRAC_SCHEMA_TABLES, GTFS_SCHEMA_TABLES

def get_stop_locations_from_transactions_and_latest_gtfs(start_date: datetime, end_date: datetime, 
    automap_base_dict: dict, transactions_t: Table | None = None) -> Select:
    '''
    This function returns a query that can be used to get transactions with their stop locations.
    The transactions table is joined with the gtfs stop locations data.
    For each stop, we get the latest GTFS feed and assign the stop location from that feed.

    Parameters
    ----------
    start_date : datetime
        Earliest possible start date for the transactions. It is imperative to add start_date for performance reasons.
    end_date : datetime
        Earliest possible end date for the transactions. It is imperative to add end_date for performance reasons.
    automap_base_dict : dict
        A dictionary containing the automap base objects for the schemas of interest
        The keys are the schema names and the values are the automap base objects
        Naming convention for key: f'Base_{schema_name_in_lowercase}'
            Use transit_equity.orca_ng.query.get_schema_key if unsure
    transactions_t : sqlalchemy.Table, optional
        Table object for the transactions table. If not provided, the default orca.transactions table is used
    
    Returns
    -------
    select : sqlalchemy.sql.selectable.Select
        A select query that can be used to get transactions with their stop locations
    
    Examples
    --------
    Example 1:
    >>> from sqlalchemy import create_engine
    >>> engine = create_engine('postgresql://user:password@localhost:5432/dbname'))
    >>> Base = get_automap_base_with_views(engine=engine, schema='orca')
    >>> transactions_t = Base_orca.metadata.tables['transactions']
    >>> query = get_stop_locations_from_transactions_and_latest_gtfs(
    ...     start_date=datetime.datetime(2023, 4, 1),
    ...     end_date=datetime.datetime(2023, 4, 30),
    ...     automap_base_dict={'Base_orca': Base_orca},
    ...     transactions_t=transactions_t
    ... )
    >>> print(type(query))
    '''
    # Keys for schemas of interest
    schemas_required = [DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA]
    schema_keys = [get_schema_key(schema_name) for schema_name in schemas_required]
    Base_dssg: AutomapBase = automap_base_dict[get_schema_key(DSSG_SCHEMA)]
    Base_trac: AutomapBase = automap_base_dict[get_schema_key(TRAC_SCHEMA)]
    Base_orca: AutomapBase = automap_base_dict[get_schema_key(ORCA_SCHEMA)]
    Base_gtfs: AutomapBase = automap_base_dict[get_schema_key(GTFS_SCHEMA)]

    if not transactions_t:
        transactions_t = Base_orca.metadata.tables[ORCA_SCHEMA_TABLES.TRANSACTIONS_TABLE]
    
    boardings_v = Base_dssg.metadata.tables[DSSG_SCHEMA_TABLES.BOARDINGS_VIEW.value]

