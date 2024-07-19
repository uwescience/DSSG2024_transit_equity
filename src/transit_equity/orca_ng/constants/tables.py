"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from enum import Enum

class DSSG_TABLES(Enum):
    '''
    Access using DSSG_TABLES.<table_name>.value
    '''
    BOARDINGS_VIEW: str = 'v_boardings_apr2023'
    TRANSACTIONS_MAT_VIEW: str = 'm_transactions_apr2023'

class ORCA_TABLES(Enum):
    '''
    Access using ORCA_TABLES.<table_name>.value
    '''
    TRANSACTIONS_TABLE: str = 'transactions',
    TRANSACTION_TYPES_TABLE: str = 'transaction_types',
    MODES_TABLE: str = 'modes'

class TRAC_TABLES(Enum):
    '''
    Access using TRAC_TABLES.<table_name>.value
    '''
    AGENCIES_TABLE: str = 'agencies'

class GTFS_TABLES(Enum):
    '''
    Access using GTFS_TABLES.<table_name>.value
    '''
    FEED_INFO_TABLE: str = 'tl_feed_info'
    FEEDS_TABLE: str = 'transitland_feeds'
    STOPS_TABLE: str = 'tl_stops'
    AGENCY_TABLE: str = 'tl_agency'
