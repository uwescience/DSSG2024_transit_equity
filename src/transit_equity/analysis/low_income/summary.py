import pandas as pd
import geopandas as gpd

def get_transactions_by_census_summary(df_transactions_with_location: pd.DataFrame, gdf_block_group_data: gpd.GeoDataFrame,
                                       ) -> pd.DataFrame:
    """
    A function to get the number of transactions per census block group.

    Parameters
    ----------
    df_transactions_with_location : pd.DataFrame
        A DataFrame containing the transactions with their locations
    
    
    """
    pass

# gdf_pg_bg_counts_summary = [f'Total Transactions: {df_transactions_with_location.shape[0]},'+ 
#                             f'Total Blocks: {gdf_block_group_transaction_counts.shape[0]}']
# gdf_pg_bg_counts_summary.append(f'Average Transactions per Block: {df_transactions_with_location.shape[0] / gdf_block_group_transaction_counts.shape[0]}')
# gdf_pg_bg_counts_summary.append(f'Min Transactions per Block: {gdf_block_group_transaction_counts["txn_count"].min()}, '+
#                                 f'Max Transactions per Block: {gdf_block_group_transaction_counts["txn_count"].max()}')
# gdf_pg_bg_counts_summary.append(f'Median Transactions per Block: {gdf_block_group_transaction_counts["txn_count"].median()}')
# gdf_pg_bg_counts_summary.append(f'\nPercentile Transactions per Block:\n{gdf_block_group_transaction_counts["txn_count"]\
#                                     .quantile([0.25, 0.5, 0.75, 0.9, 0.95, 0.99])}\n')
                                    
# print('\n'.join(gdf_pg_bg_counts_summary))