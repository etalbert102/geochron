""" Conversion from FeatureCollection to geotime datastructure """
from typing import String
from geostructures.collection import  FeatureCollection, Track
from geochron.chronnet import chronnet_create


def convert(fcol: FeatureCollection, datastructure: String):
    """
    Converts a geostructures FeatureCollection to a desired geotime datastructure
    
    Args:
        fcol: the target FeatureCollection

        datastructure: the desired datastructure currently timecube, and
        chronnet are supported

    Returns:
        Desired geotime representation
    """
    track = Track(fcol.geoshapes)

    if datastructure == "timehex":
        result = 
    elif datastructure == "chronnet":
        result = 
    else:
        print("Data structure not currently supported please check doc string for supported options")

    return result

