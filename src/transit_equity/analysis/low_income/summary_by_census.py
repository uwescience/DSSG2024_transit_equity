"""
This module contains functions to summarize transactions by census block group.

Functions
---------
get_transaction_counts_per_block_group:
    A function to get the number of transactions per census block group.

get_user_counts_per_block_group:
    A function to get the number of unique users per census block group.

get_all_counts_per_block_group:
    A function to get various counts per census block group.

get_counts_per_block_in_region:
    A function to filter out count-related dataframes by the regions they belong to

TODO: Refactor the naming convention of the function parameter/variable names to have object type as suffix.
    E.g. df_transactions_with_locations -> transactions_with_locations_df

TODO: It seems that the count-based functions are doing one extra functionality that should be separated out.
    This is the conversion of the transaction locations to a GeoDataFrame. 
    Once this is separated out, instead of df_transactions_with_locations, the function can take in a GeoDataFrame
"""

import pandas as pd
import geopandas as gpd
from shapely import wkb

from ...census.utils import TIGER_MAIN_COLUMNS

def get_transactions_geo_df(df_transactions_with_locations: pd.DataFrame, transaction_location_column: str = 'transaction_location',
                            is_transaction_location_shaped: bool = False, transaction_crs: int = 4326,) -> gpd.GeoDataFrame:
    """
    A function to convert a DataFrame containing transactions with locations to a GeoDataFrame.

    Parameters
    ----------
    df_transactions_with_locations : pd.DataFrame
        A DataFrame containing the transactions with their locations.
        One way to get this DataFrame is to use the `TransactionsWithLocations` class in the 
        `transit_equity.orca_ng.query.transactions_with_locations` module.
    
    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object

    transaction_crs : int
        The CRS of the transaction locations.
        Default is 4326 (EPSG:4326)

    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the transactions with their locations
    """
    # The transaction_location_column is a WKB hex string that needs to be converted to a Shapely geometry object
    if not is_transaction_location_shaped:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations.apply(func=lambda row: wkb.loads(bytes.fromhex(row[transaction_location_column])), axis=1) 
    else:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations[transaction_location_column]

    gdf_transactions = gpd.GeoDataFrame(data=df_transactions_with_locations, geometry="transaction_location_shape", 
                                        crs=f"EPSG:{transaction_crs}")
    return gdf_transactions

# A generic function that groups transactions (of any type, but with the same schema) by census block group
def get_transaction_counts_per_block_group(df_transactions_with_locations: str, gdf_block_group_data: gpd.GeoDataFrame,
                                           transaction_location_column = 'transaction_location', 
                                           is_transaction_location_shaped: bool = False,
                                           transaction_crs: int = 4326,
                                           census_gdf_crs: int = 32610,
                                           count_column: str = 'txn_count') -> gpd.GeoDataFrame:
    """
    A function to get the number of transactions per census block group.

    (Note: Currently, there is no explicit check to ensure that the census GeoDataFrame is for census block groups.
    Hence, in theory, this function can be used to get the number of transactions per any type of census geography.
    However, this has not been tested.)

    Parameters
    ----------
    df_transactions_with_locations : pd.DataFrame
        A DataFrame containing the transactions with their locations.
        One way to get this DataFrame is to use the `TransactionsWithLocations` class in the 
        `transit_equity.orca_ng.query.transactions_with_locations` module.
        (Note: The CRS of the transaction locations should be EPSG:4326)
        TODO: Check if it is necessary to specify the CRS of the transaction locations
    
    gdg_block_group_data : gpd.GeoDataFrame
        A GeoDataFrame containing the census block group data.
        One way to get this GeoDataFrame is to use the `get_puget_sound_block_group_data` function in the
        `transit_equity.census.puget_sound` module.
    
    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object
    
    transaction_crs : int
        The CRS of the transaction locations.
        Default is 4326 (EPSG:4326)

    census_gdf_crs : int
        The CRS of the census block group data.
        Default is 32610 (EPSG:32610)
    
    count_column : str
        The name of the column in the output GeoDataFrame that will contain the transaction count
    
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the number of transactions per census block group
    """
    gdf_transactions = get_transactions_geo_df(df_transactions_with_locations, transaction_location_column, is_transaction_location_shaped)
    gdf_transactions = gdf_transactions.to_crs(epsg=census_gdf_crs)

    gdf_transactions_bg = gpd.sjoin(gdf_transactions, gdf_block_group_data, how="left", predicate="within")
    gdf_transactions_bg_counts = gdf_transactions_bg[['txn_id', 'GEOID']].groupby(by='GEOID', axis=0).count().reset_index()\
        .rename(columns={'txn_id': count_column})
    
    gdf_block_group_transaction_counts = pd.merge(gdf_block_group_data, gdf_transactions_bg_counts, how='inner', on='GEOID')
    return gdf_block_group_transaction_counts

# A generic function that analyzes unique users per census
def get_user_counts_per_block_group(df_transactions_with_locations: str, gdf_block_group_data: gpd.GeoDataFrame,
                                           transaction_location_column = 'transaction_location', 
                                           is_transaction_location_shaped: bool = False,
                                           transaction_crs: int = 4326,
                                           census_gdf_crs: int = 32610,
                                           count_column: str = 'user_count') -> gpd.GeoDataFrame:
    """
    A function to get the number of unique users per census block group.

    (Note: Currently, there is no explicit check to ensure that the census GeoDataFrame is for census block groups.
    Hence, in theory, this function can be used to get the number of transactions per any type of census geography.
    However, this has not been tested.)

    Parameters
    ----------
    df_transactions_with_locations : pd.DataFrame
        A DataFrame containing the transactions with their locations.
        One way to get this DataFrame is to use the `TransactionsWithLocations` class in the 
        `transit_equity.orca_ng.query.transactions_with_locations` module.
        (Note: The CRS of the transaction locations should be EPSG:4326)
        TODO: Check if it is necessary to specify the CRS of the transaction locations
    
    gdg_block_group_data : gpd.GeoDataFrame
        A GeoDataFrame containing the census block group data.
        One way to get this GeoDataFrame is to use the `get_puget_sound_block_group_data` function in the
        `transit_equity.census.puget_sound` module.
    
    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object

    transaction_crs : int
        The CRS of the transaction locations.
        Default is 4326 (EPSG:4326)
    
    census_gdf_crs : int
        The CRS of the census block group data.
        Default is 32610 (EPSG:32610)

    count_column : str
        The name of the column in the output GeoDataFrame that will contain the user count
    
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the number of unique users per census block group
    """
    gdf_transactions = get_transactions_geo_df(df_transactions_with_locations, transaction_location_column, is_transaction_location_shaped)
    gdf_transactions = gdf_transactions.to_crs(epsg=census_gdf_crs)

    gdf_transactions_bg: gpd.GeoDataFrame = gpd.sjoin(gdf_transactions, gdf_block_group_data, how="left", predicate="within")

    gdf_users_bg: pd.DataFrame = gdf_transactions_bg[['txn_id', 'card_id', 'GEOID']].groupby(by=['card_id', 'GEOID'], axis=0).count().reset_index()

    gdf_users_bg_counts: pd.DataFrame = gdf_users_bg[['card_id', 'GEOID']].groupby(by='GEOID', axis=0).count().reset_index()\
        .rename(columns={'card_id': count_column})

    gdf_block_group_user_counts = pd.merge(gdf_block_group_data, gdf_users_bg_counts, how='inner', on='GEOID')

    return gdf_block_group_user_counts

def get_all_counts_per_block_group(df_transactions_with_locations: pd.DataFrame, gdf_block_group_data: gpd.GeoDataFrame,
                                   transaction_location_column = 'transaction_location',
                                   is_transaction_location_shaped: bool = False,
                                   census_gdf_crs: int = 32610,
                                   transaction_count_column: str = 'txn_count',
                                   user_count_column: str = 'user_count',
                                   merge_columns: list = None,
                                   low_income_population_df: pd.DataFrame = None,
                                   low_income_population_column: str = 'low_income_population',
                                   population_column: str = 'population') -> gpd.GeoDataFrame:
    """
    A function to get various counts per census block group.
    These counts include: 
    - Number of transactions per census block group
    - Number of unique users per census
    - Number of low-income individuals per census block group (if low_income_population_df is provided)
    - Number of individuals per census block group (if low_income_population_df is provided)
    Additional counts can be added as needed.

    Parameters
    ----------
    TODO: There are a lot of parameters here. Consider refactoring the function to take in a dictionary of parameters.
    df_transactions_with_locations : pd.DataFrame
        A DataFrame containing the transactions with their locations.
        One way to get this DataFrame is to use the `TransactionsWithLocations` class in the 
        `transit_equity.orca_ng.query.transactions_with_locations` module.
        (Note: The CRS of the transaction locations should be EPSG:4326)
    
    gdg_block_group_data : gpd.GeoDataFrame
        A GeoDataFrame containing the census block group data.
        One way to get this GeoDataFrame is to use the `get_puget_sound_block_group_data` function in the
        `transit_equity.census.puget_sound` module.

    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object
    
    census_gdf_crs : int
        The CRS of the census block group data
    
    transaction_count_column : str
        The name of the column in the output GeoDataFrame that will contain the transaction count
    
    user_count_column : str
        The name of the column in the output GeoDataFrame that will contain the user count
    
    merge_columns : list
        The columns to merge the counts-based GeoDataFrames on. 
        If None, the columns in `transit_equity.census.utils.TIGER_MAIN_COLUMNS` and 'geometry' will be used.
    
    low_income_population_df : pd.DataFrame
        A DataFrame containing the low-income population data.
        One way to get this DataFrame is to use the `get_low_income_population_data` function in the
        `transit_equity.census.puget_sound` module.

        Optional. 
        Default is None. If None, the low-income population counts will not be included in the output GeoDataFrame.
    
    low_income_population_column : str
        The name of the column in the low_income_population_df that contains the low-income population count

    population_column : str
        The name of the column in the low_income_population_df that contains the total population count
        
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the number of transactions and unique users per census block group
    """
    gdf_block_group_transaction_counts = get_transaction_counts_per_block_group(
        df_transactions_with_locations, gdf_block_group_data, 
        transaction_location_column=transaction_location_column, is_transaction_location_shaped=is_transaction_location_shaped,
        census_gdf_crs=census_gdf_crs, count_column=transaction_count_column)
    
    gdf_block_group_user_counts = get_user_counts_per_block_group(
        df_transactions_with_locations, gdf_block_group_data,
        transaction_location_column=transaction_location_column, is_transaction_location_shaped=is_transaction_location_shaped,
        census_gdf_crs=census_gdf_crs, count_column=user_count_column)
    
    if merge_columns is None:
        merge_columns = [*TIGER_MAIN_COLUMNS, 'geometry']
    
    gdf_block_group_counts = pd.merge(gdf_block_group_transaction_counts, gdf_block_group_user_counts, how='inner',
                                      on=merge_columns)
    
    if low_income_population_df is not None:
        gdf_low_income_population = gdf_block_group_data.merge(low_income_population_df, on='GEOID', how='right')
        # Keep only the necessary columns. May need to change this according to new requirements.
        gdf_low_income_population = gdf_low_income_population[
            [*TIGER_MAIN_COLUMNS, low_income_population_column, population_column, 'geometry']]
    
        gdf_block_group_counts = pd.merge(gdf_block_group_counts, gdf_low_income_population, how='outer', on=merge_columns)

    return gdf_block_group_counts


# A generic function used to filter out count-related dataframes by the regions they belong to
def get_counts_per_block_in_region(gdf_block_group_counts: gpd.GeoDataFrame, gdf_region: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    A function to filter out the block group counts by the regions they belong to.
    Not a very necessary function since it is only 1 line of code, but it is here for consistency and readability.

    Parameters
    ----------
    gdf_block_group_counts : gpd.GeoDataFrame
        A GeoDataFrame containing the block group counts
    
    gdf_region : gpd.GeoDataFrame
        A GeoDataFrame containing the regions
    
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the block group counts filtered by the regions they belong to
    """
    gdf_block_group_counts_region = gpd.sjoin(gdf_block_group_counts, gdf_region, how="inner", predicate="within")
    return gdf_block_group_counts_region