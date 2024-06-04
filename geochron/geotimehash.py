""" Geotime hash representation"""
from typing import Callable, List
from collections import Counter
from datetime import  datetime, timedelta
from geostructures.structures import ShapeBase
from geostructures.time import TimeInterval
from geostructures import FeatureCollection, Track

def precision_delta(precision: int):
    """
    Translates a timehash precision into the corresponding timedelta. 
    Args:
        precision: the desired precision of the timehash precision higher
        then 10 is not supported

    Returns:
        A timedelta
    """
    if precision == 1:
        delta = timedelta(days = 5840)
    elif precision == 2:
        delta = timedelta(days = 730)
    elif precision == 3:
        delta = timedelta(days = 91.2)
    elif precision == 4:
        delta = timedelta(days = 11.4)
    elif precision == 5:
        delta = timedelta(hours = 34.2)
    elif precision == 6:
        delta = timedelta(hours = 4.2)
    elif precision == 7:
        delta = timedelta(minutes = 32)
    elif precision == 8:
        delta = timedelta(minutes = 4)
    elif precision == 9:
        delta = timedelta(seconds = 30)
    elif precision == 10:
        delta = timedelta(seconds = 3.6)
    else:
        print("Only precision up to 10 is supported")
    return delta

def generate_times(start_time: datetime, end_time: datetime, precision: int):
    """
    Get the corresponding time list between two times with the
    interval determined by the timehash precision. 
    
    Args:
        start_time: the start time
        
        end_time: the endtime

        precision: the desired precision of the timehash precision higher
        then 10 is not supported

    Returns:
        A list of times
    """
    start = start_time
    end = end_time
    time_list = []

    while start <= end:
        time_list.append(start.timestamp())
        start += precision_delta(precision)

    return time_list




def timehash_geoshape(geoshape: ShapeBase, precision: int):
    """
    Converts a geoshape time into a  list of timehashes of varying precision. 
    A single timepoint produces a list of 1.  
    Time intervals produces a list of geotime hashes that reflect the timehashes
    that cover that time interval at the given precision.
    Args:
        geoshape: a geoshape

        precision: the desired precision of the timehash precision higher
        then 10 is not supported

    Returns:
        A timehash list
    """
    # pylint: disable=import-outside-toplevel
    import timehash
    timehash_list = []
    assert isinstance(geoshape.dt, TimeInterval)
    start_time = geoshape.dt.start
    end_time = geoshape.dt.end

    time_list = generate_times(start_time, end_time, precision)

    for time in time_list:
        timehash1 = timehash.encode(time, precision)
        timehash_list.append(timehash1)

    return timehash_list


def append_timehash_to_geohashmap(hashmap: dict, timehash_list: List):
    """
    Appends a timehash to each geohash. If there are multiple timehashes in the list
    every permutation of geohash/timehash is appended.
    Args:
        hashmap: the hashmap produced by a geographic hashing function 

        timehash_list: the associated timehashes 

    Returns:
        A geotime hashmap
    """
    geotime_hashmap = {}
    for key, value in hashmap.items():
        for item in timehash_list:
            new_key = str(key) + "_" + str(item)
            geotime_hashmap[new_key] = value
    return geotime_hashmap


def breakdown_hashmap_by_suffix(hashmap: Counter):
    """
    Breaks down a hashmap by the common suffixes. 
    Args:
        hashmap: the target hashmap 

    Returns:
        A dictionary of dictionaries with each shared suffix serving
        as the outer key
    """
    suffix_dict = {}
    for key in hashmap:
        suffix = key.split('_')[-1]  # assuming suffixes are defined after the last underscore
        if suffix not in suffix_dict:
            suffix_dict[suffix] = {key: hashmap[key]}
        else:
            suffix_dict[suffix][key] = hashmap[key]

    return suffix_dict


def combine_dicts(d:dict):
    """
    Combines a dictionary of dictionaries by dropping the outer keys
    and flattening the inner dictionaries.
    Args:
        d: A dictionary of dictionaries 

    Returns:
        A dictionary of dictionaries with each shared suffix serving
        as the outer key
    """
    combined_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            combined_dict.update(v)
        else:
            combined_dict[k] = v
    return combined_dict


def convert_geotimehash(fcol: FeatureCollection, precision: int,
     hash_func: Callable):
    """
    Converts a FeatureCollection into a chronnet by a specified timehash precision
    using a specified hashing function
    
    Args:
        fcol: a FeatureCollection with time bound shapes 

        precision: the precision of the time hash

        hash_func: the hashing function


    Returns:
        A geotime hashmap
    """
    track = Track(fcol.geoshapes)
    master_geotime_hashmap:Counter = Counter()
    shape_count:Counter = Counter()

    for shape in track:
        geohashmap = hash_func(Track([shape]))
        timehash_list = timehash_geoshape(shape, precision)
        timehash_dict = {item: 1 for item in timehash_list}
        temp_geotime_hashmap = append_timehash_to_geohashmap(geohashmap, timehash_list)
        shape_count.update(timehash_dict)
        master_geotime_hashmap.update(temp_geotime_hashmap)

    suffix_dict = breakdown_hashmap_by_suffix(master_geotime_hashmap)

    for outer_key, inner_dict in suffix_dict.items():
        num_shapes = shape_count[outer_key]
        for inner_key, value in inner_dict.items():
            inner_dict[inner_key] /= num_shapes

    return combine_dicts(suffix_dict)
