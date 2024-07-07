"""
This file contains all the table, view and materialized view names in the database, with a list for each schema.
The names are hard-coded because the database schema is static.
"""

from .schemas import DSSG_SCHEMA, ORCA_SCHEMA, TRAC_SCHEMA, GTFS_SCHEMA

def add_schema_to_tables(table_dict: dict, schema_name: str):
    return {table_key: schema_name+'.'+table_name for table_key, table_name in table_dict.items()}

DSSG_TABLES = {
    'BOARDINGS_VIEW': 'v_boardings_apr2023',
    'LINKED_TRANSACTIONS_VIEW': 'v_linked_transactions_apr2023',

    'TRANSACTIONS_MAT_VIEW': 'm_transactions_apr2023'
}
DSSG_SCHEMA_TABLES = add_schema_to_tables(DSSG_TABLES, DSSG_SCHEMA)

ORCA_TABLES = {
    'TRANSACTION_TYPES_TABLE': 'transaction_types',
    'MODES_TABLE': 'modes'
}
ORCA_SCHEMA_TABLES = add_schema_to_tables(ORCA_TABLES, ORCA_SCHEMA)

TRAC_TABLES = {
    'AGENCIES_TABLE': 'agencies'
}
TRAC_SCHEMA_TABLES = add_schema_to_tables(TRAC_TABLES, TRAC_SCHEMA)

GTFS_TABLES = {
    'FEED_INFO_TABLE': 'tl_feed_info'
}
GTFS_SCHEMA_TABLES = add_schema_to_tables(GTFS_TABLES, GTFS_SCHEMA)
