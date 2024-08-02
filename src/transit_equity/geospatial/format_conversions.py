import geopandas as gpd
from shapely import wkb
import binascii
from geopy.distance import geodesic
from branca.colormap import linear

def load_wkb(hex_string):
    """Function to decode and load WKB binary location
    into Shapely geometry object to enable plotting
    with geoPandas.
    
    Parameters
    ----------
    hex_string : object
        WKB binary object

    Returns
    -------
    object
        Shapely geometry object.

    """
    return wkb.loads(binascii.unhexlify(hex_string))

# Define a function to calculate the distance
def calculate_geodesic_distance(row):
    """
    This function takes as input a row from a dataframe with columns for boarding stop latitude and longitude and alighting stop
    latitude and longitude and returns the geodesic distance between the stops in kilometers. to be used in an apply function on a geodataframe. 

    Example: 
    # Apply the function to each row in the DataFrame
    gdf_network_clean['geo_dist'] = gdf_network_clean.apply(calculate_geodesic_distance, axis=1)
    """
    return geodesic([row['board_lat'], row['board_lon']], [row['alight_lat'], row['alight_lon']]).km

def calculate_radius(value):
    """Scale the value to a size range for determining radius of circle on folium map.

    Example: 
    # Add circle markers to the map
    for index, row in gdf_network_clean.iterrows():
        folium.CircleMarker(
            location=[row['board_lat'], row['board_lon']],
            radius=calculate_radius(row['centrality_board']),  # Set radius based on the value
            color='darkgray',  # Marker border color
            fill=True,
            fill_color='gray',  # Marker fill color
            fill_opacity=0.6,  # Marker fill opacity
            popup=f'Value: {row['centrality_board']}'
    ).add_to(mapit)
    """
    return size_range[0] + (size_range[1] - size_range[0]) * (value - min_value) / (max_value - min_value)

def create_colormap_scaled_to_var(geo_df, var_column, caption):# Create a colormap
    min_dist = geo_df[var_column].min()
    max_dist = geo_df[var_column].max()
    colormap = linear.viridis.scale(min_dist, max_dist)
    colormap.caption = caption
    return colormap