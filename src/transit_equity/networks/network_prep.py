import binascii
import pandas as pd
import geopandas as gpd
from shapely import wkb


def clean_and_filter_network_data(trips_df, hex_grid_path):
    """
    Processes a DataFrame of trip data to filter, transform, and spatially analyze trips.

    Args:
        df_trips_lift (pd.DataFrame): A DataFrame containing trip data from the sqlalchemy query already 
        filtered to a particular orca card type, with the following columns:
            - 'stop_location': The boarding location in binary string format.
            - 'stop_location_1': The alighting location in binary string format.
            - 'device_dtm_pacific': The boarding date and time.
            - 'alight_dtm_pacific': The alighting date and time.
            - 'txn_id': The boarding transaction ID.
            - 'txn_id_1': The alighting transaction ID.
        hex_grid_path (str): The file path to a shapefile containing hex grid polygons.

    Returns:
        gpd.GeoDataFrame: A cleaned GeoDataFrame with the following columns:
            - 'card_id': The ID of the card used for the trip.
            - 'trip_time_minutes': The duration of the trip in minutes.
            - 'board_centroid': The centroid of the hex grid polygon where the trip started.
            - 'alight_centroid': The centroid of the hex grid polygon where the trip ended.
            - 'trip_centroid_frequency': The frequency of trips between the boarding and alighting centroids.
            - 'number_boards': The number of times a centroid is a boarding point.
            - 'number_alights': The number of times a centroid is an alighting point.

    Steps:
        1. Rename columns for clarity.
        2. Drop true duplicate rows.
        3. Calculate the absolute difference in time between boarding and alighting.
        4. Remove duplicate trips, keeping the first instance.
        5. Filter trips to those with a duration of 3 hours or less.
        6. Convert location binary strings to shapely geometries.
        7. Convert geometries to string format.
        8. Calculate the frequency of trips between each pair of boarding and alighting locations.
        9. Merge frequency data with the original DataFrame.
        10. Drop unnecessary columns.
        11. Convert the DataFrame to a GeoDataFrame.
        12. Load and preprocess the hex grid shapefile.
        13. Perform spatial joins to associate boarding and alighting points with hex grid centroids.
        14. Merge boarding and alighting GeoDataFrames.
        15. Calculate the frequency of trips between each pair of centroids.
        16. Clean the final GeoDataFrame by removing duplicates, null values, and trips with the same boarding and alighting centroids.
        17. Add counts of how many times a centroid is a boarding or alighting point.
        18. Filter trips to those with a frequency of more than 50 trips.

    Example:
        >>> gdf_network_clean = process_trips_data(df_trips_lift, "/path/to/hex_grid.shp")
    """
    def load_wkb(x):
            return wkb.loads(binascii.unhexlify(x))
    # rename stop location columns to be more intuitive
    trips_df = trips_df.rename(columns={'stop_location':'board_location',
                                        'stop_location_1':'alight_location',
                                        'device_dtm_pacific':'board_dtm_pacific',
                                        'alight_dtm_pacific':'alight_dtm_pacific',
                                        'txn_id':'board_txn_id',
                                        'txn_id_1':'alight_txn_id',
                                        })

    # Drop true duplicate rows
    unduplicated_trips_lift = df_trips_lift.drop_duplicates()

    # Add column storing the absolute difference in time between board and alight
    unduplicated_trips_lift['trip_time_minutes'] = abs((unduplicated_trips_lift['alight_dtm_pacific'] \
                                                        - unduplicated_trips_lift['board_dtm_pacific'] \
                                                    ).dt.total_seconds() / 60)

    # Keep the first instance of duplicated rows
    drop_dupes_alight = unduplicated_trips_lift.drop_duplicates(subset=['card_id', 'board_dtm_pacific', 'alight_dtm_pacific', 'board_location', 'trip_time_minutes'], keep='first')

    #subsetting to trips less than or equal to 3 hours based on Mark and Ryan's input
    tripsize_filter_df = drop_dupes_alight[drop_dupes_alight['trip_time_minutes'] <= 180]

    # convert location binary strings to shapely geometries to enable plotting
    tripsize_filter_df['board_location_shapely'] = tripsize_filter_df['board_location'].apply(load_wkb)
    tripsize_filter_df['alight_location_shapely'] = tripsize_filter_df['alight_location'].apply(load_wkb)

    # to determine frequency between stops first need to convert geometry to string
    tripsize_filter_df['board_string'] = tripsize_filter_df['board_location'].astype('string')
    tripsize_filter_df['alight_string'] = tripsize_filter_df['alight_location'].astype('string')

    # Calculate edge frequencies for each combination of origin and destination and create column to match in tripsize filter df
    edge_freq = tripsize_filter_df.groupby(['board_string', 'alight_string']).size().reset_index(name='trip_frequency')

    # combining board and alight string to create column to match 
    edge_freq['start_stop_string'] = edge_freq['board_string'] + edge_freq['alight_string']
    edge_freq = edge_freq[['trip_frequency','start_stop_string']]

    # need to create a column to match in tripsize_filter_df
    tripsize_filter_df['start_stop_string'] = tripsize_filter_df['board_string'] + tripsize_filter_df['alight_string']

    # Merge edge_freq into tripsize_filter_df based on 'start_stop_string'
    tripsize_filter_df = pd.merge(tripsize_filter_df, edge_freq, on='start_stop_string', how='left')

    # now drop cols that we won't use any longer
    tripsize_filter_clean = tripsize_filter_df[['card_id', 'board_location', \
                                                'alight_location', 'board_location_shapely', \
                                                'alight_location_shapely', 'trip_time_minutes', \
                                                'trip_frequency', 'board_string', \
                                            'alight_string']]

    # changing pandas df to geopandas geo df
    gdf_trips = gpd.GeoDataFrame(tripsize_filter_clean, geometry='board_location_shapely')

    # Ensure shapely locations are set as geometry dtype
    gdf_trips = gdf_trips.set_geometry('board_location_shapely')

    # Set data crs (this crs is typical of Seattle, orca ng locations were in this crs)
    gdf_trips = gdf_trips.set_crs(epsg=32610) 

    # reproject to web mercator to match basemap
    gdf_trips = gdf_trips.to_crs('EPSG:3857')

    # Loading hex data from Melissa
    hex_grid_eigth_mile = gpd.read_file(hex_grid_path)

    # need to reproject to same crs as gdf_board
    hex_grid_eigth_mile = hex_grid_eigth_mile.to_crs(gdf_trips.crs.to_string())

    # calculate centroid of each polygon and set correct crs
    hex_centroids = hex_grid_eigth_mile.centroid
    hex_centroids = hex_centroids.to_crs(gdf_trips.crs.to_string())

    # add column to store the centroid geometries
    hex_grid_eigth_mile['centroid_location'] = hex_centroids

    # now need to do spatial join for each board and alight geometry to get the centroid location
    gdf_boarding = gdf_trips[['card_id', 'board_location_shapely', 'trip_time_minutes', 'trip_frequency']]

    # Ensure shapely locations are set as geometry dtype
    gdf_boarding = gdf_boarding.set_geometry('board_location_shapely')

    # reproject to web mercator to match basemap
    gdf_boarding = gdf_boarding.to_crs('EPSG:3857')

    # repeat for alights
    # now need to do spatial join for each board and alight geometry to get the centroid location
    gdf_alight = gdf_trips[['card_id', 'alight_location_shapely', 'trip_time_minutes', 'trip_frequency']]

    # Ensure shapely locations are set as geometry dtype
    gdf_alight = gdf_alight.set_geometry('alight_location_shapely')

    # reproject to web mercator to match basemap
    gdf_alight = gdf_alight.to_crs('EPSG:3857')

    # Perform a spatial join to determine which polygon each point is contained in
    gdf_boarding_poly_joined = gpd.sjoin(gdf_boarding, hex_grid_eigth_mile, how='left', predicate='within')
    # rename centroid location to boarding centroid
    gdf_boarding_poly_joined = gdf_boarding_poly_joined.rename(columns={'centroid_location':'board_centroid'})
    #drop index and rowid
    gdf_boarding_poly_joined = gdf_boarding_poly_joined[['card_id', 'board_location_shapely', 'trip_time_minutes',
        'trip_frequency','board_centroid']]

    # need to drop board_centroid == 'None'
    gdf_boarding_poly_joined = gdf_boarding_poly_joined[gdf_boarding_poly_joined['board_centroid'] != None]

    #repeat for alights
    gdf_destination_poly_joined = gpd.sjoin(gdf_alight, hex_grid_eigth_mile, how='left', predicate='within')
    gdf_destination_poly_joined = gdf_destination_poly_joined.rename(columns={'centroid_location':'alight_centroid'})
    #drop index and rowid
    gdf_destination_poly_joined = gdf_destination_poly_joined[['card_id', 'alight_location_shapely', 'trip_time_minutes',
        'trip_frequency','alight_centroid']]

    # need to drop board_centroid == 'None'
    gdf_destination_poly_joined = gdf_destination_poly_joined[gdf_destination_poly_joined['alight_centroid'] != None]

    # now need to join both geo dataframes

    gdf_board_alight_merge = gdf_boarding_poly_joined.merge(gdf_destination_poly_joined, on=['card_id', 'trip_time_minutes',
        'trip_frequency'])

    centroid_freq = gdf_board_alight_merge.groupby(['board_centroid', 'alight_centroid']).size().reset_index(name='trip_centroid_frequency')

    # now need to join back onto gdf_boarding_poly_joined
    # to determine frequency between stops first need to convert geometry to string
    gdf_board_alight_merge['board_string'] = gdf_board_alight_merge['board_centroid'].astype('string')
    gdf_board_alight_merge['alight_string'] = gdf_board_alight_merge['alight_centroid'].astype('string')
    gdf_board_alight_merge['start_stop_string'] = gdf_board_alight_merge['board_string'] + gdf_board_alight_merge['alight_string']

    # combining board and alight string to create column to match 
    centroid_freq['board_string'] = centroid_freq['board_centroid'].astype('string')
    centroid_freq['alight_string'] = centroid_freq['alight_centroid'].astype('string')
    centroid_freq['start_stop_string'] = centroid_freq['board_string'] + centroid_freq['alight_string']
    centroid_freq = centroid_freq[['trip_centroid_frequency','start_stop_string']]

    # Merge edge_freq into tripsize_filter_df based on 'start_stop_string'
    gdf_network = pd.merge(gdf_board_alight_merge, centroid_freq, on='start_stop_string', how='left')

    # select only necessary columns 
    gdf_network_clean = gdf_network[["card_id", "trip_time_minutes", "board_centroid", "alight_centroid", "trip_centroid_frequency"]]

    # double check that duplicates and nas are being dropped
    gdf_network_clean = gdf_network_clean.drop_duplicates().dropna()

    # now need to remove instances where the board_centroid and alight_centroid are the same
    gdf_network_clean = gdf_network_clean[gdf_network_clean['board_centroid'] != gdf_network_clean['alight_centroid']]

    # now want to add a column that counts how many times a particular centroid is a start or stop
    gdf_network_clean['number_boards'] = gdf_network_clean.groupby('board_centroid')['board_centroid'].transform('count')
    gdf_network_clean['number_alights'] = gdf_network_clean.groupby('alight_centroid')['alight_centroid'].transform('count')

    ## need str columns for centroid locations
    gdf_network_clean['board_string'] = gdf_network_clean['board_centroid'].astype('string')
    gdf_network_clean['alight_string'] = gdf_network_clean['alight_centroid'].astype('string')

    # Filter to only frequent trips, ones that happened more than 50 times
    gdf_network_clean = gdf_network_clean[gdf_network_clean['trip_centroid_frequency'] > 50]

    # now need to reset geometry for the geodataframe
    gdf_network_clean = gdf_network_clean.set_geometry('board_centroid')

    return gdf_network_clean
