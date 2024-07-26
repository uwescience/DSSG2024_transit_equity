"""
This module contains constants functions to get the census block data for Puget Sound

Constants
---------
CENSUS_GROUP_WASHINGTON_LINK :
    Example Link for Washington Census Block Groups

FIPS_PUGET_SOUND :
    Puget Sound Regional Council FIPS [King, Kitsap, Pierce, Snohomish]

FIPS_PUGET_SOUND_ALL :
    Puget Sound All Counties FIPS [King, Kitsap, Pierce, Snohomish, Island, Jefferson, Mason, Skagit, Thurston]

Functions
---------
get_puget_sound_block_group_data :
    Function to get the census block data for Puget Sound
"""
import geopandas as gpd

# Example Link for 
CENSUS_GROUP_WASHINGTON_LINK = \
    "https://www2.census.gov/geo/tiger/TIGER2022/BG/tl_2022_53_bg.zip"

# Puget Sound Regional Council FIPS [King, Kitsap, Pierce, Snohomish]
FIPS_PUGET_SOUND = ['033', '035','053','061']

# Puget Sound All Counties FIPS [King, Kitsap, Pierce, Snohomish, Island, Jefferson, Mason, Skagit, Thurston]
FIPS_PUGET_SOUND_ALL = ['033', '035','053','061', '029', '031', '045', '057', '067']

def get_puget_sound_block_group_data(
        block_group_wa_link: str = CENSUS_GROUP_WASHINGTON_LINK,
        fips_list: list = FIPS_PUGET_SOUND
    ):
    """
    A function to get the census block data for Puget Sound
    """
    # Access shapefile of Washington census block groups
    gdf_wa_block_group = gpd.read_file(block_group_wa_link)

    gdf_puget_sound_block_group = gdf_wa_block_group[gdf_wa_block_group['COUNTYFP'].isin(fips_list)]

    return gdf_puget_sound_block_group