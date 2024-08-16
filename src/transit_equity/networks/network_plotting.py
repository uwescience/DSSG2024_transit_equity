"""
Module for geographic data processing and visualization of trip networks.

This module provides a set of functions for calculating geodesic distances between
geographic points, scaling node size values for map visualizations, and creating colormaps
for spatial data. These functions are particularly useful in the context of 
network analysis and geographic data visualization.

Functions
---------
- calculate_geodesic_distance_km(row)
    Calculates the geodesic distance between two geographic points (boarding and alighting) in 
    kilometers.
    
- calculate_node_radius(df, col_name, value, lower_bound, upper_bound)
    Scales a value to a specified range based on the minimum and maximum values of a column in a 
    DataFrame.

- create_colormap_scaled_to_var(geo_df, var_column, caption)
    Creates a colormap scaled to the minimum and maximum values of a specified variable in a 
    GeoDataFrame.

-  plot_network_edges(gdf, edge_color_var, edge_color_caption):
        Plots a network of edges representing origin-destination trips on a Folium map, with edge 
        colors determined by a specified variable. A colormap legend is also added to the map.


Usage
-----
These functions are designed to assist in preprocessing geographic data and
facilitating its visualization in spatial analysis workflows. They can be used
to calculate the shortest distance between two points on Earth, normalize node
sizes for plotting in a map, and generate color maps for a more intuitive display
of spatial variation in data.

Example
-------
You can use these functions as part of your geographic data processing pipeline. For example:

>>> gdf['distance_km'] = gdf.apply(calculate_geodesic_distance_km, axis=1)
>>> gdf['node_radius'] = 
    gdf.apply(lambda row: calculate_node_radius(gdf, 'value_col', row['value_col'], 5, 15), axis=1)
>>> colormap = create_colormap_scaled_to_var(gdf, 'distance_km', 'Trip Distance (km)')
>>> network_map = 
    plot_network_edges(gdf_trips, edge_color_var='distance_km', edge_color_caption='Distance (km)')
"""
from geopy.distance import geodesic
from branca.colormap import linear
import folium

def calculate_geodesic_distance_km(row):
    """
    Calculate the geodesic distance between two geographic points (boarding and alighting) in 
    kilometers.

    This function uses the geodesic method from the geopy library to calculate the shortest distance
    over the Earth's surface between two points specified by latitude and longitude.

    Parameters
    ----------
    row : pandas.Series
        A row of a DataFrame containing the latitude and longitude of the boarding and alighting 
        locations.
        - 'board_lat' : float
        - 'board_lon' : float
        - 'alight_lat' : float
        - 'alight_lon' : float

    Returns
    -------
    float
        The geodesic distance between the boarding and alighting points in kilometers.
    """
    return geodesic([row['board_lat'], row['board_lon']], [row['alight_lat'], row['alight_lon']]).km

def calculate_node_radius(df,
                          col_name,
                          value,
                         lower_bound,
                         upper_bound):
    """
    Scale a value to a specified range based on the minimum and maximum values of a column.

    This function normalizes the input value to a range between `lower_bound` and `upper_bound`,
    based on the minimum and maximum values present in the specified column of the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data to be normalized.
    col_name : str
        The name of the column whose values will be used for scaling.
    value : numeric
        The value to be scaled based on the column's range.
    lower_bound : numeric
        The lower bound of the output scale.
    upper_bound : numeric
        The upper bound of the output scale.

    Returns
    -------
    numeric
        The scaled value between `lower_bound` and `upper_bound`.
    """
    max_value = df[col_name].max()
    min_value = df[col_name].min()
    size_range = (lower_bound, upper_bound)
    return size_range[0] + (size_range[1] - size_range[0]) * \
        (value - min_value) / (max_value - min_value)

def create_colormap_scaled_to_var(geo_df, var_column, caption):
    """
    Create a colormap scaled to the minimum and maximum values of a specified variable.

    This function generates a colormap (from the viridis color scheme) that scales between the
    minimum and maximum values of a specified column in the GeoDataFrame. The colormap can
    then be used to visualize data variation in a map.

    Parameters
    ----------
    geo_df : geopandas.GeoDataFrame
        The GeoDataFrame containing the variable to be scaled.
    var_column : str
        The name of the column in the GeoDataFrame to be scaled and represented by the colormap.
    caption : str
        A caption or label for the colormap, typically describing the variable it represents.

    Returns
    -------
    branca.colormap.LinearColormap
        A colormap object that can be used to visualize the specified variable in the GeoDataFrame.
    """
    min_dist = geo_df[var_column].min()
    max_dist = geo_df[var_column].max()
    colormap = linear.viridis.scale(min_dist, max_dist)
    colormap.caption = caption
    return colormap

def plot_network_edges(gdf, edge_color_var, edge_color_caption):
    """
    Plots a network of edges (trip paths) on a Folium map, with edge colors representing a variable 
    of interest.

    This function generates a Folium map centered on a specified location (Seattle, WA) and plots 
    the edges of a network representing origin-destination trip pairs. Each edge (trip path) is 
    colored according to a variable of interest from the input GeoDataFrame, and a colormap legend 
    is added to the map.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        A GeoDataFrame containing the trip data with origin-destination coordinates and the variable 
        to color the edges by. Must contain the following columns:
        - 'board_lat': Latitude of the boarding location.
        - 'board_lon': Longitude of the boarding location.
        - 'alight_lat': Latitude of the alighting location.
        - 'alight_lon': Longitude of the alighting location.
        - The column specified by `edge_color_var`: The variable used to color the edges.
    
    edge_color_var : str
        The name of the column in the GeoDataFrame representing the variable to be used for coloring
        the edges.
    
    edge_color_caption : str
        The caption for the colormap legend that will be displayed on the map.

    Returns
    -------
    folium.Map
        A Folium map object with the plotted network edges and a colormap legend.

    Example
    -------
    >>> gdf_network_clean = clean_and_filter_network_data(trip_df)
    >>> network_map = plot_network_edges(gdf_network_clean, edge_color_var='distance_km', 
        edge_color_caption='Distance (km)')
    >>> network_map.save('network_map.html')
    """
    mapit = folium.Map(location=[47.6062, -122.3321], zoom_start=9.25, control_scale=True, \
                       width=500)
    folium.TileLayer('cartodbpositron').add_to(mapit)

    colormap = create_colormap_scaled_to_var(gdf, edge_color_var, edge_color_caption)

    # Adding segments between origin and destination
    for index, row in gdf.iterrows():
        folium.PolyLine(
            locations=([row['board_lat'], row['board_lon']], \
                        [row['alight_lat'], row['alight_lon']]), \
            color=colormap(row[edge_color_var])
        ).add_to(mapit)

    # Add the colormap legend to the map
    mapit.add_child(colormap)
    return mapit
