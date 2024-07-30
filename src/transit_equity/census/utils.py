"""
This module contains some utility functions to work with census data

Functions
---------
get_geo_id:
    Get the GEOID column for a census DataFrame
"""
import pandas as pd

def get_geo_id(census_df: pd.DataFrame, state_col: str = 'state', county_col: str = 'county', 
               tract_col: str = 'tract', block_group_col: str = 'block group') -> pd.DataFrame:
    """
    Get the GEOID column for a census DataFrame

    Parameters
    ----------
    census_df : pd.DataFrame
        The census DataFrame
    
    state_col : str
        The name of the column that contains the state data
    
    county_col : str
        The name of the column that contains the county data
    
    tract_col : str
        The name of the column that contains the tract data
    
    block_group_col : str
        The name of the column that contains the block group data
    
    Returns
    -------
    pd.Series
        A pandas Series containing the GEOID values
    """
    geo_id_col = census_df.apply(
        lambda row: row[state_col] + row[county_col] + row[tract_col] + row[block_group_col], axis=1)
    return geo_id_col