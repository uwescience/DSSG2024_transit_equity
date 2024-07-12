import geopandas as gpd
from shapely import wkb
import binascii

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