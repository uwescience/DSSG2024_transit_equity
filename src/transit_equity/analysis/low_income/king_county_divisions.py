"""
This module contains functions to divide King County into regions based on geography, or other factors 
"""
import pandas as pd
import geopandas as gpd
from shapely import geometry

# Cities and Unincorporated King County
KING_COUNTY_GIS_PATH = "https://gis-kingcounty.opendata.arcgis.com/datasets/3fdb7c41de8548c5ab5f96cb1ef303e2_446.geojson"

# Group Object IDs for King County that will serve as the main divisions. 
# These objects are relatively large areas that either can contain other areas, 
# or are significant enough to be considered as a separate division.
MAIN_GROUP_OBJECT_IDS = [60, 89, 49]

# The object ID for the vertical division of the areas of King County not covered by the MAIN_GROUP_OBJECT_IDS
# As mentioned, this is hard-coded logic, and there may not be any plans to change this in the future.
VERTICAL_DIVISION_OBJECT_ID = 88

def get_southmost_point(polygon: geometry.Polygon):
    exterior_coords = polygon.exterior.coords
    southernmost_point = min(exterior_coords, key=lambda coord: coord[1])
    return southernmost_point

def get_king_county_divisions(division_column: str = 'division') -> gpd.GeoDataFrame:
    """
    Get the divisions of King County based on geography.
    The divisions are based on cities and unincorporated King County.
    The logic to divide King County is currently hardcoded in this function. 
    The idea is to simply divide King County into comparable regions for more detailed and manageable analysis.
    
    There may not be any plans to change this logic in the future, but it is important to note that this is a hardcoded logic.

    Parameters
    ----------
    division_column : str
        The name of the column to store the division values

    Returns
    -------
    gpd.GeoDataFrame
        A GeoDataFrame containing the divisions of King County.
        These division values are provided in a separate column provided by the division_column parameter. 
    """
    gdf_king_county = gpd.read_file(KING_COUNTY_GIS_PATH)
    gdf_king_county = gdf_king_county.to_crs("EPSG:32610")

    gdf_kc_divisions = []
    division_id = 0
    # Divide King County based on the MAIN_GROUP_OBJECT_IDS
    for group_object_id in MAIN_GROUP_OBJECT_IDS:
        division_id += 1
        kc_division = gdf_king_county[gdf_king_county['OBJECTID']==group_object_id].iloc[0].geometry.exterior.convex_hull
        gdf_kc_division = gdf_king_county[gdf_king_county.within(kc_division)]
        gdf_kc_division[division_column] = division_id
        gdf_kc_divisions.append(gdf_kc_division)
    
    gdf_kc_outer = gdf_king_county.loc[~gdf_king_county.index.isin([index for index in pd.concat(gdf_kc_divisions).index])]

    # Divide the remaining areas of King County based on the VERTICAL_DIVISION_OBJECT_ID
    vertical_division = get_southmost_point(
        gdf_kc_outer[gdf_kc_outer['OBJECTID']==VERTICAL_DIVISION_OBJECT_ID].iloc[0].geometry
    )

    # First, get the areas that are above the vertical division
    gdf_kc_upper = gdf_kc_outer.loc[gdf_kc_outer.apply(
        lambda row: get_southmost_point(row.geometry)[1] > vertical_division[1], axis=1
    )]
    # Warning: The following line was hard-coded because the object ID 9 was not connected to the upper division.
    gdf_kc_upper = gdf_kc_upper[gdf_kc_upper['OBJECTID']!=9]
    division_id += 1
    gdf_kc_upper[division_column] = division_id
    gdf_kc_divisions.append(gdf_kc_upper)

    # Second, get the areas that are below the vertical division
    gdf_kc_lower = gdf_kc_outer.loc[~gdf_kc_outer.index.isin(gdf_kc_upper.index)]
    division_id += 1
    gdf_kc_lower[division_column] = division_id
    gdf_kc_divisions.append(gdf_kc_lower)

    return pd.concat(gdf_kc_divisions, axis=0)


