"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
In this file, the schema name is attached to the names, which is necessary if we want to use the automap_base_with_views
The names are hard-coded because the database schema is static.
"""

from enum import Enum

from .schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA

class DSSG_SCHEMA_TABLES(Enum):
    '''
    Access using DSSG_SCHEMA_TABLES.<table_name>.value
    '''
    V_BOARDINGS_APR2023: str = f'{DSSG_SCHEMA}.v_boardings_apr2023'
    V_LINKED_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.v_linked_transactions_apr2023'
    M_TRANSACTIONS_APR2023: str = f'{DSSG_SCHEMA}.m_transactions_apr2023' 

    BOARDINGS_VIEW: str = f'{DSSG_SCHEMA}.v_boardings_apr2023'
    LINKED_TRANSACTIONS_VIEW: str = f'{DSSG_SCHEMA}.v_linked_transactions_apr2023'
    TRANSACTIONS_MAT_VIEW: str = f'{DSSG_SCHEMA}.m_transactions_apr2023'

class ORCA_SCHEMA_TABLES(Enum):
    '''
    Access using ORCA_SCHEMA_TABLES.<table_name>.value
    '''
    TRANSACTIONS: str = f'{ORCA_SCHEMA}.transactions'
    TRANSACTION_TYPES: str = f'{ORCA_SCHEMA}.transaction_types'
    MODES: str = f'{ORCA_SCHEMA}.modes'

    TRANSACTIONS_TABLE: str = f'{ORCA_SCHEMA}.transactions',
    TRANSACTION_TYPES_TABLE: str = f'{ORCA_SCHEMA}.transaction_types',
    MODES_TABLE: str = f'{ORCA_SCHEMA}.modes'

class TRAC_SCHEMA_TABLES(Enum):
    '''
    Access using TRAC_SCHEMA_TABLES.<table_name>.value
    '''
    AGENCIES: str = f'{TRAC_SCHEMA}.agencies'

    AGENCIES_TABLE: str = f'{TRAC_SCHEMA}.agencies'

class GTFS_SCHEMA_TABLES(Enum):
    '''
    Access using GTFS_SCHEMA_TABLES.<table_name>.value
    '''
    TL_FEED_INFO: str = f'{GTFS_SCHEMA}.tl_feed_info'
    TRANSITLAND_FEEDS: str = f'{GTFS_SCHEMA}.transitland_feeds'
    TL_STOPS: str = f'{GTFS_SCHEMA}.tl_stops'
    TL_AGENCY: str = f'{GTFS_SCHEMA}.tl_agency'

    FEED_INFO_TABLE: str = f'{GTFS_SCHEMA}.tl_feed_info'
    FEEDS_TABLE: str = f'{GTFS_SCHEMA}.transitland_feeds'
    STOPS_TABLE: str = f'{GTFS_SCHEMA}.tl_stops'
    AGENCY_TABLE: str = f'{GTFS_SCHEMA}.tl_agency'
