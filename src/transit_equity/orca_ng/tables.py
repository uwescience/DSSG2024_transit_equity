"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from .schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA

DSSG_TABLES = {
    'TRANSACTIONS_MAT_VIEW': DSSG_SCHEMA + '.' + 'm_transactions_apr2023',
    'BOARDINGS_VIEW': DSSG_SCHEMA + '.' + 'v_boardings_apr2023',
    'LINKED_TRANSACTIONS_VIEW': DSSG_SCHEMA + '.' + 'v_linked_transactions_apr2023'
}
