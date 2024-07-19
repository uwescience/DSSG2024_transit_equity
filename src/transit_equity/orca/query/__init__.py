"""
This package stores common queries used on the orca database
"""

def get_schema_key(schema_name: str) -> str:
    return f'Base_{schema_name}'