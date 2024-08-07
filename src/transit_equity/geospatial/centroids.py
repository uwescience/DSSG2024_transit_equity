"""
This module provides functions for processing geospatial transit data to
assign boarding and alighting stops to hexagon centroids, merge these stops,
and filter trips based on frequency.

Functions:
----------
1. import_hexgrid(postgres_url, table_name):
    Import and convert a hex grid table from a PostgreSQL database to a GeoDataFrame.

2. get_hex_centroids(geo_df, hex_geo_df):
    Calculate the centroids of hexagons in a GeoDataFrame and reproject them to match the CRS of 
    another GeoDataFrame.

3. assign_stops_to_hex_centroids(geo_df, hex_grid_with_centroids, stop_type):
    Assign boarding or alighting stops to hexagon centroids by performing a spatial join.

4. merge_and_filter_trip_centroids_gdf(boardings_centroids,
                                        alights_centroids, 
                                        trip_frequency_cutoff=0):
    Merge boarding and alighting centroids, calculate trip frequencies between centroids,
    and filter the resulting GeoDataFrame based on a trip frequency cutoff.
"""
import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from transit_equity.geospatial.format_conversions import load_wkb
from transit_equity.utils.db_helpers import get_automap_base_with_views

def import_hexgrid(postgres_url,
                   table_name):
    """
    Import and convert a hex grid table from a PostgreSQL database to a GeoDataFrame.

    This function connects to a PostgreSQL database, retrieves a hex grid table, converts
    the WKB geometry data to Shapely objects, and returns a GeoDataFrame.

    Parameters
    ----------
    postgres_url : str
        The URL for connecting to the PostgreSQL database.
    table_name : str
        The name of the hex grid table to be imported.

    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the hex grid data with geometries set to the appropriate CRS.

    Notes
    -----
    The CRS of the GeoDataFrame is set to EPSG:32610. This was the CRS that the hexgrid was created
    in.
    """

    engine = create_engine(os.getenv(postgres_url))

    # Setup Session Maker and Session
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    # DSSG Schema Base
    base_dssg = get_automap_base_with_views(engine=engine, schema='dssg')

    # Hex grid table
    hex_grid_400m = base_dssg.metadata.tables[table_name]

    # query the geometry column 
    hex_query = (session.query(hex_grid_400m.c.wkb_geometry))

    hex_table = pd.read_sql(hex_query.statement, engine)

    #convert geom to shapely object
    hex_table['wkb_geometry'] = hex_table['wkb_geometry'].apply(load_wkb)

    hex_gdf = gpd.GeoDataFrame(hex_table, geometry='wkb_geometry')

    # assign crs (this was the crs when this particular hex grid was created, if using a different
    # hex grid, will need to update)
    hex_gdf = hex_gdf.set_crs(epsg=32610)

    return hex_gdf

def get_hex_centroids(geo_df, hex_geo_df):
    """
    Calculate the centroids of hexagons in a GeoDataFrame and reproject them to match the CRS of 
    another GeoDataFrame.

    Parameters:
    geo_df (GeoDataFrame): A GeoDataFrame whose CRS will be used for reprojecting the hexagon 
        centroids. Should contain stop location data.
    hex_geo_df (GeoDataFrame): A GeoDataFrame containing a grid of hexagon geometries to calculate
        centroids for.

    Returns:
    GeoDataFrame: A GeoDataFrame with the hexagon multipolygon geometry and an additional column
    'centroid_location' containing the centroid geometries of the hexagons, reprojected to the CRS
    of `geo_df`.
    
    Steps:
    1. Reproject `hex_geo_df` to the CRS of `geo_df`.
    2. Calculate the centroid of each hexagon in the reprojected GeoDataFrame.
    3. Reproject the centroids to match the CRS of `geo_df`.
    4. Add a new column 'centroid_location' to `hex_geo_df` to store the centroid geometries.

    Example:
    hex_centroids_gdf = get_hex_centroids(trips_gdf, hex_gdf)
    """
    # need to reproject to same crs as geo_df
    hex_400m = hex_geo_df.to_crs(geo_df.crs.to_string())

    # calculate centroid of each polygon and set correct crs to match gdf
    hex_centroids = hex_400m.centroid
    hex_centroids = hex_centroids.to_crs(geo_df.crs.to_string())

    # add column to store the centroid geometries
    hex_400m['centroid_location'] = hex_centroids
    return hex_400m

def assign_stops_to_hex_centroids(geo_df, hex_grid_with_centroids, stop_type):
    """
    Assigns boarding or alighting stops to hexagon centroids by performing a spatial join.

    Parameters:
    geo_df (GeoDataFrame): A GeoDataFrame containing stop data with geometries for boarding or
        alighting locations.
    hex_grid_with_centroids (GeoDataFrame): A GeoDataFrame containing hexagon geometries and their
        corresponding centroids.
    stop_type (str): A string indicating the type of stop to process, either 'board' for boarding
        stops or 'alight' for alighting stops.

    Returns:
    GeoDataFrame: A GeoDataFrame with stop data assigned to the corresponding hexagon centroids,
        including the columns: 'card_id', 'location_column', 'trip_time_minutes', 'trip_frequency',
        and the assigned centroid column ('board_centroid' or 'alight_centroid').

    Steps:
    1. Select the relevant columns based on the `stop_type`.
    2. Ensure the location column is set as the geometry type and reproject to the appropriate CRS.
    3. Perform a spatial join to determine which hexagon each stop is contained in.
    4. Rename the centroid location column based on the `stop_type`.
    5. Drop rows where the centroid is None and return the resulting GeoDataFrame.
    """

    if stop_type == 'board':
        location_column = 'board_location_shapely'
    elif stop_type == 'alight':
        location_column = 'alight_location_shapely'

    #select relevant cols
    gdf_boarding = geo_df[['card_id', location_column, 'trip_time_minutes',
                        'trip_frequency']]

    # Ensure shapely locations are set as geometry dtype
    gdf_boarding = gdf_boarding.set_geometry(location_column)

    # Set correct crs
    if gdf_boarding.crs is None:
        gdf_boarding = gdf_boarding.set_crs(epsg=32610)

    # reproject to web mercator to match basemap
    gdf_boarding = gdf_boarding.to_crs('EPSG:3857')

    # Perform a spatial join to determine which polygon each point is contained in
    gdf_boarding_poly_joined = gpd.sjoin(gdf_boarding, hex_grid_with_centroids, how='left',
                                         predicate='within')

    if stop_type == 'board':
        centroid_col_name = 'board_centroid'
    elif stop_type == 'alight':
        centroid_col_name = 'alight_centroid'

    # rename centroid location to boarding centroid
    gdf_boarding_poly_joined = \
        gdf_boarding_poly_joined.rename(columns={'centroid_location':centroid_col_name})

    #drop index and rowid
    gdf_boarding_poly_joined = gdf_boarding_poly_joined[['card_id', location_column,
                                                          'trip_time_minutes','trip_frequency',
                                                          centroid_col_name]]

    #need to drop board_centroid == 'None'
    gdf_boarding_poly_joined = \
        gdf_boarding_poly_joined[gdf_boarding_poly_joined[centroid_col_name].notnull()]

    return gdf_boarding_poly_joined

def merge_and_filter_trip_centroids_gdf(boardings_centroids,
                                        alights_centroids,
                                        trip_frequency_cutoff=0):
    """
    Merge boarding and alighting centroids, calculate trip frequencies between centroids,
    and filter the resulting GeoDataFrame based on a trip frequency cutoff. The trip frequency 
    cutoff is set to 0 unless specified.

    Parameters:
    boardings_centroids (GeoDataFrame): A GeoDataFrame containing boarding stop data with centroids.
    alights_centroids (GeoDataFrame): A GeoDataFrame containing alighting stop data with centroids.
    trip_frequency_cutoff (int, optional): The minimum frequency of trips between centroids to 
    include in the output. Default is 0, which includes all trips.

    Returns:
    GeoDataFrame: A GeoDataFrame containing the merged and filtered trip data with columns:
                  'card_id', 'trip_time_minutes', 'board_centroid', 'alight_centroid',
                  'trip_centroid_frequency', 'number_boards', 'number_alights',
                  'board_lon', 'board_lat', 'alight_lon', and 'alight_lat'.
    
    Steps:
    1. Merge the boarding and alighting GeoDataFrames on 'card_id', 'trip_time_minutes', and
        'trip_frequency'.
    2. Calculate the frequency of trips between each pair of centroids.
    3. Create string representations of the centroid geometries to facilitate merging.
    4. Merge the trip frequencies back onto the merged GeoDataFrame.
    5. Clean the resulting GeoDataFrame by dropping duplicates, rows with missing values, and trips
        where the boarding and alighting centroids are the same.
    6. Add columns counting the number of times each centroid is a boarding or alighting point.
    7. Filter the GeoDataFrame to only include trips with a frequency higher than the specified
        cutoff.
    8. Set the geometry column to 'board_centroid' and reproject to latitude and longitude.
    9. Extract the coordinates for the boarding and alighting centroids.
    """
    # now need to join both geo dataframes
    gdf_board_alight_merge = boardings_centroids.merge(alights_centroids,
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

    # Filter to only frequent trips as specified by trip_frequency_cutoff
    gdf_network_clean = gdf_network_clean[gdf_network_clean['trip_centroid_frequency'] > \
                                          trip_frequency_cutoff]

    # now need to reset geometry for the geodataframe
    gdf_network_clean = gdf_network_clean.set_geometry('board_centroid')

    # now reprojecting to lat and long
    gdf_network_clean['board_latlong'] = gdf_network_clean['board_centroid'].to_crs(4326)
    gdf_network_clean['alight_latlong'] = gdf_network_clean['alight_centroid'].to_crs(4326)

    # extracting coordinates for boardings and alights
    gdf_network_clean['board_lon'] = gdf_network_clean.board_latlong.apply(lambda p: p.x)
    gdf_network_clean['board_lat'] = gdf_network_clean.board_latlong.apply(lambda p: p.y)
    gdf_network_clean['alight_lon'] = gdf_network_clean.alight_latlong.apply(lambda p: p.x)
    gdf_network_clean['alight_lat'] = gdf_network_clean.alight_latlong.apply(lambda p: p.y)

    return gdf_network_clean
