"""
This package provides tools for processing geospatial transit data, including functions
to handle hexagon centroids and format conversions for geographic data.

Modules:
--------
1. centroids.py:
    - Functions to calculate hexagon centroids, assign stops to these centroids, and merge and filter trip data based on centroids.

2. format_conversions.py:
    - Functions to handle format conversions for geographic data, such as loading WKB binary data into Shapely geometry objects.

centroids.py:
-------------
Functions:
----------
1. get_hex_centroids(geo_df, hex_geo_df):
    Calculate the centroids of hexagons in a GeoDataFrame and reproject them to match the CRS of another GeoDataFrame.

2. assign_stops_to_hex_centroids(geo_df, hex_grid_with_centroids, stop_type):
    Assign boarding or alighting stops to hexagon centroids by performing a spatial join.

3. merge_and_filter_trip_centroids_gdf(boardings_centroids, alights_centroids, trip_frequency_cutoff=0):
    Merge boarding and alighting centroids, calculate trip frequencies between centroids,
    and filter the resulting GeoDataFrame based on a trip frequency cutoff.

format_conversions.py:
----------------------
Functions:
----------
1. load_wkb(hex_string):
    Decode and load WKB binary data into a Shapely geometry object to enable plotting with GeoPandas.

Detailed Descriptions:
----------------------
centroids.py:
-------------
1. get_hex_centroids(geo_df, hex_geo_df):
    This function takes a GeoDataFrame containing hexagon geometries and another GeoDataFrame to match the CRS.
    It calculates the centroids of the hexagons and adds them as a new column in the hexagon GeoDataFrame.
    
    Parameters:
    - geo_df (GeoDataFrame): A GeoDataFrame whose CRS will be used for reprojecting the hexagon centroids.
    - hex_geo_df (GeoDataFrame): A GeoDataFrame containing hexagon geometries to calculate centroids for.

    Returns:
    - GeoDataFrame: A GeoDataFrame with an additional column 'centroid_location' containing the centroid geometries of the hexagons, reprojected to the CRS of `geo_df`.

2. assign_stops_to_hex_centroids(geo_df, hex_grid_with_centroids, stop_type):
    This function assigns boarding or alighting stops to hexagon centroids by performing a spatial join. It processes the stops based on the type ('board' or 'alight'), sets the correct CRS, reprojects to match the base map, and filters the resulting GeoDataFrame.
    
    Parameters:
    - geo_df (GeoDataFrame): A GeoDataFrame containing stop data with geometries for boarding or alighting locations.
    - hex_grid_with_centroids (GeoDataFrame): A GeoDataFrame containing hexagon geometries and their corresponding centroids.
    - stop_type (str): A string indicating the type of stop to process, either 'board' for boarding stops or 'alight' for alighting stops.

    Returns:
    - GeoDataFrame: A GeoDataFrame with stop data assigned to the corresponding hexagon centroids, including the columns: 'card_id', 'location_column', 'trip_time_minutes', 'trip_frequency', and the assigned centroid column ('board_centroid' or 'alight_centroid').

3. merge_and_filter_trip_centroids_gdf(boardings_centroids, alights_centroids, trip_frequency_cutoff=0):
    This function merges boarding and alighting centroids, calculates trip frequencies between centroids, and filters the resulting GeoDataFrame based on a specified trip frequency cutoff. It ensures the geometries are set correctly, merges the data, calculates frequencies, and extracts coordinates for further analysis.
    
    Parameters:
    - boardings_centroids (GeoDataFrame): A GeoDataFrame containing boarding stop data with centroids.
    - alights_centroids (GeoDataFrame): A GeoDataFrame containing alighting stop data with centroids.
    - trip_frequency_cutoff (int, optional): The minimum frequency of trips between centroids to include in the output. Default is 0, which includes all trips.

    Returns:
    - GeoDataFrame: A GeoDataFrame containing the merged and filtered trip data with columns: 'card_id', 'trip_time_minutes', 'board_centroid', 'alight_centroid', 'trip_centroid_frequency', 'number_boards', 'number_alights', 'board_lon', 'board_lat', 'alight_lon', and 'alight_lat'.

format_conversions.py:
----------------------
1. load_wkb(hex_string):
    This function decodes a WKB (Well-Known Binary) hex string and loads it into a Shapely geometry object, enabling further geospatial processing and plotting with GeoPandas.
    
    Parameters:
    - hex_string (object): WKB binary object.

    Returns:
    - object: Shapely geometry object.
"""