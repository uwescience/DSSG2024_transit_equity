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

    load_wkb(x):
        Decodes and loads WKB binary location data into a Shapely geometry object for plotting with 
        GeoPandas.
        Args:
            x (object): WKB binary object.
        Returns:
            object: Shapely geometry object.

Example usage:
    import pandas as pd
    import geopandas as gpd
    from transit_equity.networks.network_prep import clean_and_filter_network_data, 
                                                        get_hex_centroids_for_od, 
                                                        load_wkb

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
