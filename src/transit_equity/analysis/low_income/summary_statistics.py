"""

"""
import pandas as pd
import geopandas as gpd

def summarize_census_block_counts_df(df_transactions_with_location: pd.DataFrame, 
                                     gdf_block_group_counts: gpd.GeoDataFrame,
                                     summary_column: str = 'txn_count',
                                     percentiles: list = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]) -> list:
    """
    Summarize the counts of transactions per census block group.

    Parameters
    ----------
    df_transactions_with_location : pd.DataFrame
        A DataFrame containing the transactions with their locations
    
    gdf_block_group_counts : gpd.GeoDataFrame
        A GeoDataFrame containing the counts of any summary column per census block group
    
    summary_column : str
        The name of the column in the GeoDataFrame that contains the summary counts
    
    percentiles : list
        A list of percentiles to calculate for the summary column
    
    Returns
    -------
    list
        A list of strings containing the summary statistics
    """
    gdf_summary = [f'Total Transactions: {df_transactions_with_location.shape[0]},'+ 
                            f'Total Blocks: {gdf_block_group_counts.shape[0]}']
    gdf_summary.append(f'Average Transactions per Block: {df_transactions_with_location.shape[0] / gdf_block_group_counts.shape[0]}')
    gdf_summary.append(f'Min Counts per Block: {gdf_block_group_counts[summary_column].min()}, '+
                                    f'Max Counts per Block: {gdf_block_group_counts[summary_column].max()}')
    gdf_summary.append(f'Median Counts per Block: {gdf_block_group_counts[summary_column].median()}')
    gdf_summary.append(f'\nPercentile Counts per Block:\n{gdf_block_group_counts[summary_column]\
                                        .quantile(percentiles)}\n')
    
    return gdf_summary