"""
Module for processing and analyzing trip data with spatial geometries.

This module contains functions to clean, filter, and analyze trip data, particularly in the context 
of mapping origin-destination pairs to hexagon centroids and calculating the frequency of trips 
between these centroids.

Functions:
    clean_and_filter_network_data(trips_df):
        Cleans and filters trip data, converting location data to Shapely geometries, and calculates
          trip frequencies.
        Args:
            trips_df (pd.DataFrame): DataFrame containing trip data.
        Returns:
            gpd.GeoDataFrame: GeoDataFrame with cleaned and filtered trip data.
        


Example usage:
    import pandas as pd
    import geopandas as gpd
    from transit_equity.networks.network_prep import clean_and_filter_network_data

    # Load trip data
    trips_df = pd.read_sql(query.statement,         #sql alchemy query 
                            engine_ng)              #sql alchemy database engine

    # Clean and filter trip data
    gdf_trips = clean_and_filter_network_data(trips_df)

"""

import pandas as pd
import geopandas as gpd
from transit_equity.geospatial.format_conversions import load_wkb

def clean_and_filter_network_data(trips_df):
    """
    Cleans and filters trip data, transforming it into a GeoDataFrame for spatial analysis.

    Args:
    trips_df (pd.DataFrame): DataFrame containing trip data with columns:
        - 'stop_location': Boarding location as a binary string.
        - 'stop_location_1': Alighting location as a binary string.
        - 'device_dtm_pacific': Boarding date and time.
        - 'alight_dtm_pacific': Alighting date and time.
        - 'txn_id': Boarding transaction ID.
        - 'txn_id_1': Alighting transaction ID.
        - 'card_id': ID of the card used for the trip.

    Returns:
    gpd.GeoDataFrame: Cleaned GeoDataFrame with columns:
        - 'card_id': ID of the card used for the trip.
        - 'board_location': Original boarding location binary string.
        - 'alight_location': Original alighting location binary string.
        - 'board_location_shapely': Shapely geometry of the boarding location.
        - 'alight_location_shapely': Shapely geometry of the alighting location.
        - 'trip_time_minutes': Duration of the trip in minutes.
        - 'trip_frequency': Frequency of trips between the boarding and alighting locations.
        - 'board_string': String representation of the boarding location.
        - 'alight_string': String representation of the alighting location.

    Steps:
        1. Rename columns for clarity.
        2. Drop true duplicate rows.
        3. Calculate the absolute difference in time between boarding and alighting.
        4. Remove duplicate trips, keeping the first instance.
        5. Filter trips to those with a duration of 3 hours or less.
        6. Convert location binary strings to Shapely geometries.
        7. Convert geometries to string format.
        8. Calculate the frequency of trips between each pair of boarding and alighting locations.
        9. Merge frequency data with the original DataFrame.
        10. Drop unnecessary columns.
        11. Convert the DataFrame to a GeoDataFrame.
        12. Set the CRS to EPSG:32610 and reproject to EPSG:3857.

    Example:
    >>> gdf_trips = clean_and_filter_network_data(df_trips_lift)"""
    # rename stop location columns to be more intuitive
    trips_df = trips_df.rename(columns={'stop_location':'board_location',
        'stop_location_1':'alight_location',
        'device_dtm_pacific':'board_dtm_pacific',
        'alight_dtm_pacific':'alight_dtm_pacific',
        'txn_id':'board_txn_id',
        'txn_id_1':'alight_txn_id',
        })

    # Drop true duplicate rows
    unduplicated_trips_lift = trips_df.drop_duplicates()

    # Add column storing the absolute difference in time between board and alight
    unduplicated_trips_lift['trip_time_minutes'] = \
        abs((unduplicated_trips_lift['alight_dtm_pacific'] - \
             unduplicated_trips_lift['board_dtm_pacific']).dt.total_seconds() / 60)

    # Keep the first instance of duplicated rows
    drop_dupes_alight = unduplicated_trips_lift.drop_duplicates(subset=['card_id',
                                                                        'board_dtm_pacific',
                                                                        'alight_dtm_pacific',
                                                                        'board_location', 
                                                                        'trip_time_minutes'],
                                                                        keep='first')

    #subsetting to trips less than or equal to 3 hours based on Mark and Ryan's input
    tripsize_filter_df = drop_dupes_alight[drop_dupes_alight['trip_time_minutes'] <= 180]

    # convert location binary strings to shapely geometries to enable plotting
    tripsize_filter_df['board_location_shapely'] = \
        tripsize_filter_df['board_location'].apply(load_wkb)
    tripsize_filter_df['alight_location_shapely'] = \
        tripsize_filter_df['alight_location'].apply(load_wkb)

    # to determine frequency between stops first need to convert geometry to string
    tripsize_filter_df['board_string'] = tripsize_filter_df['board_location'].astype('string')
    tripsize_filter_df['alight_string'] = tripsize_filter_df['alight_location'].astype('string')

    # Calculate edge frequencies for each combination of origin and destination and create column
    # to match in tripsize filter df
    edge_freq = tripsize_filter_df.groupby(['board_string', 'alight_string']) \
        .size().reset_index(name='trip_frequency')

    # combining board and alight string to create column to match
    edge_freq['start_stop_string'] = edge_freq['board_string'] + edge_freq['alight_string']
    edge_freq = edge_freq[['trip_frequency','start_stop_string']]

    # need to create a column to match in tripsize_filter_df
    tripsize_filter_df['start_stop_string'] = tripsize_filter_df['board_string'] \
        + tripsize_filter_df['alight_string']

    # Merge edge_freq into tripsize_filter_df based on 'start_stop_string'
    tripsize_filter_df = pd.merge(tripsize_filter_df, edge_freq, on='start_stop_string', how='left')

    # now drop cols that we won't use any longer
    tripsize_filter_clean = tripsize_filter_df[['card_id', 'board_location', \
                                                'alight_location', 'board_location_shapely', \
                                                'alight_location_shapely', 'trip_time_minutes', \
                                                'trip_frequency', 'board_string', \
                                                'alight_string'
                                                ]]

    # changing pandas df to geopandas geo df
    gdf_trips = gpd.GeoDataFrame(tripsize_filter_clean, geometry='board_location_shapely')

    # Ensure shapely locations are set as geometry dtype
    gdf_trips = gdf_trips.set_geometry('board_location_shapely')

    # Set data crs (this crs is typical of Seattle, orca ng locations were in this crs)
    gdf_trips = gdf_trips.set_crs(epsg=32610)

    # reproject to web mercator to match basemap
    gdf_trips = gdf_trips.to_crs('EPSG:3857')

    return gdf_trips