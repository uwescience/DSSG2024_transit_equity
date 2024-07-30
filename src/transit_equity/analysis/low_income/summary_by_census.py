"""
This module contains functions to summarize transactions by census block group.

Functions
---------
get_transaction_counts_per_block_group:
    A function to get the number of transactions per census block group.

get_user_counts_per_block:
    A function to get the number of unique users per census block group.
"""

import pandas as pd
import geopandas as gpd
from shapely import wkb

# A generic function that groups transactions (of any type, but with the same schema) by census block group
def get_transaction_counts_per_block_group(df_transactions_with_locations: str, gdf_block_group_data: gpd.GeoDataFrame,
                                           transaction_location_column = 'transaction_location', 
                                           is_transaction_location_shaped: bool = False,
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
        A DataFrame containing the transactions with their locations
        (Note: The CRS of the transaction locations should be EPSG:4326)
        TODO: Check if it is necessary to specify the CRS of the transaction locations
    
    gdg_block_group_data : gpd.GeoDataFrame
        A GeoDataFrame containing the census block group data
    
    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object
    
    census_gdf_crs : int
        The CRS of the census block group data
    
    count_column : str
        The name of the column in the output GeoDataFrame that will contain the transaction count
    
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the number of transactions per census block group
    """

    # The transaction_location_column is a WKB hex string that needs to be converted to a Shapely geometry object
    if not is_transaction_location_shaped:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations.apply(func=lambda row: wkb.loads(bytes.fromhex(row[transaction_location_column])), axis=1) 
    else:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations[transaction_location_column]

    gdf_transactions = gpd.GeoDataFrame(data=df_transactions_with_locations, geometry="transaction_location_shape", crs="EPSG:4326")
    gdf_transactions = gdf_transactions.to_crs(epsg=census_gdf_crs)

    gdf_transactions_bg = gpd.sjoin(gdf_transactions, gdf_block_group_data, how="left", predicate="within")
    gdf_transactions_bg_counts = gdf_transactions_bg[['txn_id', 'GEOID']].groupby(by='GEOID', axis=0).count().reset_index()\
        .rename(columns={'txn_id': count_column})
    
    gdf_block_group_transaction_counts = pd.merge(gdf_block_group_data, gdf_transactions_bg_counts, how='inner', on='GEOID')
    return gdf_block_group_transaction_counts

# A generic function that analyzes unique users per census
def get_user_counts_per_block(df_transactions_with_locations: str, gdf_block_group_data: gpd.GeoDataFrame,
                                           transaction_location_column = 'transaction_location', 
                                           is_transaction_location_shaped: bool = False,
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
        A DataFrame containing the transactions with their locations
        (Note: The CRS of the transaction locations should be EPSG:4326)
        TODO: Check if it is necessary to specify the CRS of the transaction locations
    
    gdg_block_group_data : gpd.GeoDataFrame
        A GeoDataFrame containing the census block group data
    
    transaction_location_column : str
        The column name in the DataFrame that contains the transaction location
    
    is_transaction_location_shaped : bool
        A flag to indicate if the transaction location is already a Shapely geometry object
    
    census_gdf_crs : int
        The CRS of the census block group data
    
    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the number of unique users per census block group
    """
    
    # The transaction_location_column is a WKB hex string that needs to be converted to a Shapely geometry object
    if not is_transaction_location_shaped:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations.apply(func=lambda row: wkb.loads(bytes.fromhex(row[transaction_location_column])), axis=1) 
    else:
        df_transactions_with_locations['transaction_location_shape'] = \
            df_transactions_with_locations[transaction_location_column]

    gdf_transactions = gpd.GeoDataFrame(data=df_transactions_with_locations, geometry="transaction_location_shape", crs="EPSG:4326")
    gdf_transactions = gdf_transactions.to_crs(epsg=census_gdf_crs)

    gdf_transactions_bg: gpd.GeoDataFrame = gpd.sjoin(gdf_transactions, gdf_block_group_data, how="left", predicate="within")

    gdf_users_bg: pd.DataFrame = gdf_transactions_bg[['txn_id', 'card_id', 'GEOID']].groupby(by=['card_id', 'GEOID'], axis=0).count().reset_index()

    gdf_users_bg_counts: pd.DataFrame = gdf_users_bg[['card_id', 'GEOID']].groupby(by='GEOID', axis=0).count().reset_index()\
        .rename(columns={'card_id': count_column})

    gdf_block_group_user_counts = pd.merge(gdf_block_group_data, gdf_users_bg_counts, how='inner', on='GEOID')

    return gdf_block_group_user_counts

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