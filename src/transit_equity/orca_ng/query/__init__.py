"""
This package stores common queries used on the orca_ng database

Modules:
--------
transactions_with_locations:
    This module contains the TransactionsWithLocations class that can be used to get transactions with their stop locations.

get_stop_location: 
    Deprecation Warning: 
        This file is deprecated due to its restrictive nature. Consider using transactions_with_locations module instead.
    This module contains a function that returns a query to get transactions with their stop locations.
"""

def get_schema_key(schema_name: str) -> str:
    return f'Base_{schema_name}'