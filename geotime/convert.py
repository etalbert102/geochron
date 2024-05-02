""" Conversion from FeatureCollection to geotime datastructure """
from typing import String
from geostructures.collection import Track
from geotime.chronnet import chronnet_create
from geotime.timecube import TimeCube

def convert(collection: Track, datastructure: String):
    """
    Converts a geostructures Track to a desired geotime datastructure
    
    Args:
        collection: the target FeatureCollection for conversion

        datastructure: the desired datastructure currently timecube, and
        chronnet are supported

    Returns:
        Desired geotime representation
    """ 
    if datastructure == "timecube":
        result = 
    elif datastructure == "chronnet":
        result = 
    else:
        print("Data structure not currently supported please check doc string for supported options")

    return result