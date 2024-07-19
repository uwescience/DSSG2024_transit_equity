"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from enum import Enum

class DSSG_TABLES(Enum):
    """
    Access using DSSG_TABLES.<table_name>.value
    """
    V_BOARDINGS_APR2023: str = 'v_boardings_apr2023'
    V_LINKED_TRANSACTIONS_APR2023: str = 'v_linked_transactions_apr2023'
    M_TRANSACTIONS_APR2023: str = 'm_transactions_apr2023'

    BOARDINGS_VIEW: str = 'v_boardings_apr2023'
    LINKED_TRANSACTIONS_VIEW: str = 'v_linked_transactions_apr2023'
    TRANSACTIONS_MAT_VIEW: str = 'm_transactions_apr2023'

class ORCA_TABLES(Enum):
    """
    Access using ORCA_TABLES.<table_name>.value
    """
    TRANSACTIONS: str = 'transactions'
    TRANSACTION_TYPES: str = 'transaction_types'
    MODES: str = 'modes'

    TRANSACTIONS_TABLE: str = 'transactions',
    TRANSACTION_TYPES_TABLE: str = 'transaction_types',
    MODES_TABLE: str = 'modes'

class TRAC_TABLES(Enum):
    """
    Access using TRAC_TABLES.<table_name>.value
    """
    AGENCIES: str = 'agencies'

    AGENCIES_TABLE: str = 'agencies'

class GTFS_TABLES(Enum):
    """
    Access using GTFS_TABLES.<table_name>.value
    """
    TL_FEED_INFO: str = 'tl_feed_info'
    TRANSITLAND_FEEDS: str = 'transitland_feeds'
    TL_STOPS: str = 'tl_stops'
    TL_AGENCY: str = 'tl_agency'

    FEED_INFO_TABLE: str = 'tl_feed_info'
    FEEDS_TABLE: str = 'transitland_feeds'
    STOPS_TABLE: str = 'tl_stops'
    AGENCY_TABLE: str = 'tl_agency'
