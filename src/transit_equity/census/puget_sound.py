import geopandas as gpd

# Example Link for 
CENSUS_GROUP_WASHINGTON_LINK = \
    "https://www2.census.gov/geo/tiger/TIGER2022/BG/tl_2022_53_bg.zip"

# Puget Sound FIPS
FIPS_PUGET_SOUND = ['033', '035','053','061']

def get_puget_sound_block_group_data(
        block_group_wa_link: str = CENSUS_GROUP_WASHINGTON_LINK
    ):
    '''
    A function to get the census block data for Puget Sound
    '''
    # Access shapefile of Washington census block groups
    gdf_wa_block_group = gpd.read_file(block_group_wa_link)

    gdf_puget_sound_block_group = gdf_wa_block_group[gdf_wa_block_group['COUNTYFP'].isin(FIPS_PUGET_SOUND)]

    return gdf_puget_sound_block_group