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
        
    get_hex_centroids_for_od(geo_df, hex_grid_path):
        Processes trip data to map origin-destination pairs to hexagon centroids and calculates the 
        frequency of trips between these centroids.
        Args:
            geo_df (gpd.GeoDataFrame): GeoDataFrame containing trip data.
            hex_grid_path (str): Path to the shapefile containing the hexagonal grid.
        Returns:
            gpd.GeoDataFrame: GeoDataFrame with origin-destination centroids and trip frequencies.


Example usage:
    import pandas as pd
    import geopandas as gpd
    from transit_equity.networks.network_prep import clean_and_filter_network_data, 
                                                        get_hex_centroids_for_od

    # Load trip data
    trips_df = pd.read_sql(query.statement,         #sql alchemy query 
                            engine_ng)              #sql alchemy database engine

    # Clean and filter trip data
    gdf_trips = clean_and_filter_network_data(trips_df)

    # Define path to hex grid shapefile
    hex_grid_path = 'path_to_hex_grid.shp'

    # Map origin-destination pairs to hexagon centroids and calculate frequencies
    gdf_network_clean = get_hex_centroids_for_od(gdf_trips, hex_grid_path)
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



def get_hex_centroids_for_od_trips(geo_df, hex_grid_path):
    """
    Processes trip data to map origin-destination pairs to hexagon centroids and calculates the 
    frequency of trips between these centroids.

    Args:
    geo_df (gpd.GeoDataFrame): GeoDataFrame containing trip data with the following columns:
        - 'card_id': ID of the card used for the trip.
        - 'board_location_shapely': Shapely geometry of the boarding location.
        - 'alight_location_shapely': Shapely geometry of the alighting location.
        - 'trip_time_minutes': Duration of the trip in minutes.
        - 'trip_frequency': Frequency of trips between the boarding and alighting locations.
   hex_grid_path (str): Path to the shapefile containing the hexagonal grid.

    Returns:
    gpd.GeoDataFrame: GeoDataFrame containing the following columns:
        - 'card_id': ID of the card used for the trip.
        - 'trip_time_minutes': Duration of the trip in minutes.
        - 'board_centroid': Shapely geometry of the boarding centroid.
        - 'alight_centroid': Shapely geometry of the alighting centroid.
        - 'trip_centroid_frequency': Frequency of trips between the centroids.
        - 'number_boards': Count of trips starting at each boarding centroid.
        - 'number_alights': Count of trips ending at each alighting centroid.
        - 'board_string': String representation of the boarding centroid.
        - 'alight_string': String representation of the alighting centroid.

    Steps:
        1. Load hexagonal grid data.
        2. Reproject hexagonal grid to match the CRS of `geo_df`.
        3. Calculate centroids of hexagons.
        4. Perform spatial joins to associate each boarding and alighting location with a hexagon
         centroid.
        5. Calculate the frequency of trips between centroids.
        6. Merge trip frequency data back into the GeoDataFrame.
        7. Filter and clean the data to remove duplicates, null values, and trips where the start 
         and stop centroids are the same.
        8. Add columns to count the number of trips starting or ending at each centroid.
        9. Filter to only include frequent trips (more than 50 occurrences).
        10. Set the geometry to the boarding centroid for the final GeoDataFrame.

    Example:
    >>> gdf_network_clean = get_hex_centroids_for_od(trip_geo_df, "path/to/hex_grid.shp")
    """
    # Loading hex data
    hex_grid_eigth_mile = gpd.read_file(hex_grid_path)

    # need to reproject to same crs as geo_df
    hex_grid_eigth_mile = hex_grid_eigth_mile.to_crs(geo_df.crs.to_string())

    # calculate centroid of each polygon and set correct crs
    hex_centroids = hex_grid_eigth_mile.centroid
    hex_centroids = hex_centroids.to_crs(geo_df.crs.to_string())

    # add column to store the centroid geometries
    hex_grid_eigth_mile['centroid_location'] = hex_centroids

    # now need to do spatial join for each board and alight geometry to get the centroid location
    gdf_boarding = geo_df[['card_id', 'board_location_shapely', 'trip_time_minutes',
                            'trip_frequency']]

    # Ensure shapely locations are set as geometry dtype
    gdf_boarding = gdf_boarding.set_geometry('board_location_shapely')

    # reproject to web mercator to match basemap
    gdf_boarding = gdf_boarding.to_crs('EPSG:3857')

    # repeat for alights
    # now need to do spatial join for each board and alight geometry to get the centroid location
    gdf_alight = geo_df[['card_id', 'alight_location_shapely', 'trip_time_minutes',
                          'trip_frequency']]

    # Ensure shapely locations are set as geometry dtype
    gdf_alight = gdf_alight.set_geometry('alight_location_shapely')

    # reproject to web mercator to match basemap
    gdf_alight = gdf_alight.to_crs('EPSG:3857')

    # Perform a spatial join to determine which polygon each point is contained in
    gdf_boarding_poly_joined = gpd.sjoin(gdf_boarding, hex_grid_eigth_mile, how='left',
                                          predicate='within')
    # rename centroid location to boarding centroid
    gdf_boarding_poly_joined = \
        gdf_boarding_poly_joined.rename(columns={'centroid_location':'board_centroid'})
    #drop index and rowid
    gdf_boarding_poly_joined = gdf_boarding_poly_joined[['card_id', 'board_location_shapely',
                                                          'trip_time_minutes','trip_frequency',
                                                          'board_centroid']]

    # need to drop board_centroid == 'None'
    gdf_boarding_poly_joined = \
        gdf_boarding_poly_joined[gdf_boarding_poly_joined['board_centroid'] is not None]

    #repeat for alights
    gdf_destination_poly_joined = gpd.sjoin(gdf_alight, hex_grid_eigth_mile, how='left',
                                             predicate='within')
    gdf_destination_poly_joined = \
        gdf_destination_poly_joined.rename(columns={'centroid_location':'alight_centroid'})
    #drop index and rowid
    gdf_destination_poly_joined = gdf_destination_poly_joined[['card_id', 'alight_location_shapely',
                                                                'trip_time_minutes',
                                                                'trip_frequency',
                                                                'alight_centroid']]

    # need to drop board_centroid == 'None'
    gdf_destination_poly_joined = \
        gdf_destination_poly_joined[gdf_destination_poly_joined['alight_centroid'] is not None]

    # now need to join both geo dataframes
    gdf_board_alight_merge = gdf_boarding_poly_joined.merge(gdf_destination_poly_joined,
                                                             on=['card_id', 'trip_time_minutes',
                                                                 'trip_frequency'])

    centroid_freq = gdf_board_alight_merge.groupby(['board_centroid', 'alight_centroid'])\
        .size().reset_index(name='trip_centroid_frequency')

    # now need to join back onto gdf_boarding_poly_joined
    # to determine frequency between stops first need to convert geometry to string
    gdf_board_alight_merge['board_string'] = \
        gdf_board_alight_merge['board_centroid'].astype('string')
    gdf_board_alight_merge['alight_string'] = \
        gdf_board_alight_merge['alight_centroid'].astype('string')
    gdf_board_alight_merge['start_stop_string'] = \
        gdf_board_alight_merge['board_string'] + gdf_board_alight_merge['alight_string']

    # combining board and alight string to create column to match
    centroid_freq['board_string'] = centroid_freq['board_centroid'].astype('string')
    centroid_freq['alight_string'] = centroid_freq['alight_centroid'].astype('string')
    centroid_freq['start_stop_string'] = \
        centroid_freq['board_string'] + centroid_freq['alight_string']
    centroid_freq = centroid_freq[['trip_centroid_frequency','start_stop_string']]

    # Merge edge_freq into tripsize_filter_df based on 'start_stop_string'
    gdf_network = pd.merge(gdf_board_alight_merge, centroid_freq, on='start_stop_string',
                            how='left')

    # select only necessary columns
    gdf_network_clean = gdf_network[["card_id", "trip_time_minutes", "board_centroid",
                                      "alight_centroid", "trip_centroid_frequency"]]

    # double check that duplicates and nas are being dropped
    gdf_network_clean = gdf_network_clean.drop_duplicates().dropna()

    # now need to remove instances where the board_centroid and alight_centroid are the same
    gdf_network_clean = \
        gdf_network_clean[gdf_network_clean['board_centroid'] != \
                          gdf_network_clean['alight_centroid']]

    # now want to add a column that counts how many times a particular centroid is a start or stop
    gdf_network_clean['number_boards'] = \
        gdf_network_clean.groupby('board_centroid')['board_centroid'].transform('count')
    gdf_network_clean['number_alights'] = \
        gdf_network_clean.groupby('alight_centroid')['alight_centroid'].transform('count')

    ## need str columns for centroid locations
    gdf_network_clean['board_string'] = gdf_network_clean['board_centroid'].astype('string')
    gdf_network_clean['alight_string'] = gdf_network_clean['alight_centroid'].astype('string')

    # Filter to only frequent trips, ones that happened more than 50 times
    gdf_network_clean = gdf_network_clean[gdf_network_clean['trip_centroid_frequency'] > 50]

    # now need to reset geometry for the geodataframe
    gdf_network_clean = gdf_network_clean.set_geometry('board_centroid')

    return gdf_network_clean
