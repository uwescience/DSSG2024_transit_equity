"""
Module for processing and analyzing trip data from the orca_ng database for network analysis.

This module contains functions to pull, clean, and filter trip data from the orca_ng 
database, transforming it into a GeoDataFrame for spatial network analysis.

Functions
---------
get_trip_tables_by_cardtype(postgres_url_ng, test_schema, orca_schema, trips_table, 
                            alights_table, boardings_table, transactions_table, 
                            vboardings_table, gtfs_table, user_type)
    Pulls and processes trips table data from the orca_ng database based on user type.

clean_and_filter_network_data(trips_df)
    Cleans and filters trip data, transforming it into a GeoDataFrame for spatial analysis.
"""
import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from transit_equity.geospatial.format_conversions import load_wkb
from transit_equity.utils.db_helpers import get_automap_base_with_views

def get_trip_tables_by_cardtype(postgres_url_ng,
                                test_schema,
                                orca_schema,
                                trips_table,
                                alights_table,
                                boardings_table,
                                vboardings_table,
                                gtfs_table,
                                user_type,
                                chunk_size=100000):
    """
    Pull and process trips table data from the orca_ng database based on user type.

    This function connects to the orca_ng database, constructs a query to pull trip data,
    processes the data in chunks, filters and cleans the data, and returns a GeoDataFrame
    containing the trip data.

    Parameters
    ----------
    postgres_url_ng : str
        The URL for connecting to the PostgreSQL database.
    test_schema : str
        The schema name containing test tables.
    orca_schema : str
        The schema name containing ORCA-related tables.
    trips_table : str
        The name of the trips table.
    alights_table : str
        The name of the alights table.
    boardings_table : str
        The name of the boardings table.
    transactions_table : str
        The name of the transactions table.
    vboardings_table : str
        The name of the view boardings table.
    gtfs_table : str
        The name of the GTFS stops table.
    user_type : str
        The passenger type ID used to filter the data. In the orca_ng table, the groups are as
        follows:
            1 = Adult
            2 = Youth
            3 = Senior
            4 = Disabled
            5 = Low Income
        Note: This may need to be updated if the codes were changed between the new ORCA db and 
        orca_ng. I think that the new ORCA db uses letters to signify the card types, and that the 
        column name that stores the passenger types may be named differently. Double check if this 
        is true when using the updated database.
    chunk_size : int
        The number of rows in each chunk. Defaults to 100000.
    
    Returns
    -------
    GeoDataFrame
        A GeoDataFrame containing the trip data, with geometries set to 'board_location_shapely'.
    """

    #connect to engines
    engine_ng = create_engine(os.getenv(postgres_url_ng))

    # Setup Session Maker and Session
    session_ng_maker = sessionmaker(bind=engine_ng)
    session_ng = session_ng_maker()

    # NG test Schema Base
    base_ng_test = get_automap_base_with_views(engine=engine_ng, schema=test_schema)
    base_ng_orca = get_automap_base_with_views(engine=engine_ng, schema=orca_schema)

    # Tables of interest from orca_ng
    trips_ng = base_ng_test.metadata.tables[trips_table]
    alights_ng = base_ng_test.metadata.tables[alights_table]
    boardings_ng = base_ng_test.metadata.tables[boardings_table]
    vboardings_ng = base_ng_orca.metadata.tables[vboardings_table]
    gtfs_stops_ng = base_ng_test.metadata.tables[gtfs_table]

    # Constructing the query
    query = (
        session_ng.query(
            vboardings_ng.c.card_id,
            vboardings_ng.c.txn_id,
            alights_ng.c.txn_id,
            vboardings_ng.c.device_dtm_pacific,
            alights_ng.c.alight_dtm_pacific,
            boardings_ng.c.stop_location,
            gtfs_stops_ng.c.stop_location
        ).select_from(trips_ng)
        .join(boardings_ng, boardings_ng.c.txn_id == trips_ng.c.orig_txn_id)
        .join(alights_ng, alights_ng.c.txn_id == trips_ng.c.dest_txn_id)
        .join(vboardings_ng, vboardings_ng.c.txn_id == trips_ng.c.orig_txn_id)
        .join(gtfs_stops_ng, gtfs_stops_ng.c.stop_id == alights_ng.c.stop_id)
        .filter(
            and_(
                boardings_ng.c.stop_location.isnot(None),
                gtfs_stops_ng.c.stop_location.isnot(None),
                vboardings_ng.c.passenger_type_id == user_type
            )
        )
    )

    # Because the adults table is so large that it was causing memory limitation issues, read the
    # table in chunks of chunk_size rows and then concatenate them after.


    with engine_ng.connect() as connection:
        result_proxy = connection.execution_options(stream_results=True).execute(query.statement)
        chunk_count = 0
        chunks = []

        while True:
            chunk = result_proxy.fetchmany(chunk_size)
            if not chunk:
                break
            chunk_df = pd.DataFrame(chunk, columns=result_proxy.keys())
            # Filter and clean each chunk here, can trade out for other cleaning pipeline for other
            # analyses if desired
            filtered_chunk_gdf = clean_and_filter_network_data(chunk_df)
            chunks.append(filtered_chunk_gdf)
            chunk_count += 1
            # Print progress for each 10 chunks read.
            if chunk_count % 10 == 0:
                print(f"Fetched chunk {chunk_count}")

    # Concatenate all chunks into a single DataFrame
    df_trips_lift = pd.concat(chunks, ignore_index=True)
    print(f"Total records fetched: {len(df_trips_lift)}")

    # changing pandas df to geopandas geo df
    df_trips_gdf = gpd.GeoDataFrame(df_trips_lift, geometry='board_location_shapely')

    # Ensure shapely locations are set as geometry dtype
    gdf_trips = df_trips_gdf.set_geometry('board_location_shapely')

    return gdf_trips

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
