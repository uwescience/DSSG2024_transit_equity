"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from enum import Enum

class DSSG_TABLES(Enum):
    BOARDINGS_VIEW: str = 'v_boardings_apr2023'
    LINKED_TRANSACTIONS_VIEW: str = 'v_linked_transactions_apr2023'
    TRANSACTIONS_MAT_VIEW: str = 'm_transactions_apr2023'

class ORCA_TABLES(Enum):
    TRANSACTION_TYPES_TABLE: str = 'transaction_types',
    MODES_TABLE: str = 'modes'

class TRAC_TABLES(Enum):
    AGENCIES_TABLE: str = 'agencies'

class GTFS_TABLES(Enum):
    FEED_INFO_TABLE: str = 'tl_feed_info'
