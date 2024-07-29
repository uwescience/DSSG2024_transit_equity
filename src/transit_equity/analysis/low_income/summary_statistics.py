"""
This module contains functions to get various summary statistics for the low income analysis.

Functions:
----------
summarize_census_block_counts_df:
    Summarize different counts and statistics of transactions per census block group.
"""
import pandas as pd
import geopandas as gpd

def get_summary_census_block_counts_df(df_transactions_with_location: pd.DataFrame, 
                                     gdf_block_group_counts: gpd.GeoDataFrame,
                                     summary_column: str = 'txn_count',
                                     percentiles: list = None,
                                     transaction_label: str = 'Transaction') -> list:
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
    if not percentiles:
        percentiles = [0.25, 0.5, 0.75, 0.9, 0.95, 0.99]

    summary = [f'Total {transaction_label}s: {df_transactions_with_location.shape[0]},'+ 
                            f'Total Blocks: {gdf_block_group_counts.shape[0]}']
    summary.append(f'Average {transaction_label}s per Block: {df_transactions_with_location.shape[0] / gdf_block_group_counts.shape[0]}')
    summary.append(f'Min {transaction_label}s per Block: {gdf_block_group_counts[summary_column].min()}, '+
                                    f'Max {transaction_label}s per Block: {gdf_block_group_counts[summary_column].max()}')
    summary.append(f'Median {transaction_label}s per Block: {gdf_block_group_counts[summary_column].median()}')
    summary.append(f'\nPercentile {transaction_label}s per Block:\n{gdf_block_group_counts[summary_column]\
                                        .quantile(percentiles)}\n')
    
    return summary