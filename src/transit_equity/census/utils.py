"""
This module contains some utility functions to work with census data

Constants
---------
TIGER_MAIN_COLUMNS :
    The main columns that are present in the TIGER shapefiles

Functions
---------
get_geo_id:
    Get the GEOID column for a census DataFrame
"""
import pandas as pd
from census import Census
from dotenv import load_dotenv

TIGER_MAIN_COLUMNS = ['STATEFP', 'COUNTYFP', 'TRACTCE', 'BLKGRPCE', 'GEOID']

def get_census(path_env: str, census_api_key: str = 'CENSUS_API_KEY') -> Census:
    """
    Get the Census object using the API key

    Parameters
    ----------
    path_env : str
        Path to the .env file that contains the environment variables
    
    census_api_key : str
        The key for the environment variable that contains the census API key
    
    Returns
    -------
    Census
        A Census object that is connected to the API
    
    Examples
    --------
    Example 1:
    >>> census = get_census('.env', 'CENSUS_API_KEY')
    >>> print(type(census))
    <class 'census.core.Census'>
    """
    load_dotenv(dotenv_path=path_env)
    census = Census(census_api_key)
    return census

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