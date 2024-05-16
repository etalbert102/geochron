""" Conversion from FeatureCollection to geotime datastructure """
from geostructures.collections import  FeatureCollection, Track
from geostructures.geohash import H3Hasher
from geochron.chronnet import convert_chronnet
from geochron.timehex import convert_timehex
from geochron.geotimehash import convert_geotimehash

def convert(fcol: FeatureCollection, datastructure: str,
            hour_interval: float, res= int(10), **kwargs):
    """
    Converts a geostructures FeatureCollection to a desired geotime datastructure
    
    Args:
        fcol: the target FeatureCollection

        datastructure: the desired datastructure currently timehex, and
        chronnet are supported

        hour_interval: the length in hours of the desired interval

        res: the resolution of the hashing function if using the
        default H3 hashing function      

    Keyword Args:
        hash_func: (Callable) (Default H3 hasher)
            The hashing function that is used
        self_loop: (bool) (Default True)
            Applies to chronnets only whether self loops
            are included
        mode: (str) (Default directed)
            Applies to chronnets only whether network is
            directed or not

    Returns:
        Desired geotime representation
    """
    track = Track(fcol.geoshapes)
    hasher = H3Hasher(resolution = res)
    hashing_function = kwargs.get('hash_func', hasher.hash_collection)
    if datastructure == "timehex":
        result = convert_timehex(track, hour_interval, hashing_function)
    elif datastructure == "chronnet":
        self_loop = kwargs.get('self_loop', True)
        mode = kwargs.get('mode', "directed")
        result = convert_chronnet(track, hour_interval, hashing_function, self_loop, mode)
    elif datastructure == "geotimehash":
        precision = kwargs.get('precision')
        if precision is None:
            print("need the precision keyword for this data structure")
        assert isinstance(precision, int)
        result = convert_geotimehash(track, precision, hashing_function)
    else: # pragma: no cover
        print("Data structure not supported please check doc string for supported options")

    return result
