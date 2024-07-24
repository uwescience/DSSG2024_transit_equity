import pandas as pd
import geopandas as gpd
from shapely import wkb

# A generic function that groups transactions (of any type, but with the same schema) by census block group
def get_transaction_counts_per_block_group(df_transactions_with_locations: str, gdf_block_group_data: gpd.GeoDataFrame,
                                           transaction_location_column = 'transaction_location', 
                                           is_transaction_location_shaped: bool = False,
                                           census_gdf_crs: int = 32610) -> gpd.GeoDataFrame:
    """
    A function to get the number of transactions per census block group

    Parameters
    ----------
    df_transactions_with_locations : pd.DataFrame
        A DataFrame containing the transactions with their locations
    
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
        .rename(columns={'txn_id': 'txn_count'})
    
    gdf_block_group_counts = pd.merge(gdf_block_group_data, gdf_transactions_bg_counts, how='inner', on='GEOID')
    return gdf_block_group_counts