""" Geotime hash representation"""
from typing import Callable
from collections import Counter
from datetime import  datetime, timedelta
import timehash
from geostructures.structures import GeoShape
from geostructures import Track

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
        delta = timedelta(years = 16)
    elif precision == 2:
        delta = timedelta(years = 2)
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




def timehash_geoshape(geoshape: GeoShape, precision: int):
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
    timehash_list = []
    start_time = geoshape.dt.start
    end_time = geoshape.dt.end

    time_list = generate_times(start_time, end_time, precision)

    for time in time_list: 
        timehash1 = timehash.encode(time, precision)
        timehash_list.append(timehash1)
    
    return timehash_list


def append_timehash_to_geohashmap(hashmap, timehash_list):
    geotime_hashmap = {}
    for key, value in hashmap.items():
        for item in timehash_list:
            new_key = str(key) + "_" + str(item)
            geotime_hashmap[new_key] = value
    return geotime_hashmap


def breakdown_hashmap_by_suffix(hashmap: Counter):
    suffix_dict = {}
    for key in hashmap:
        suffix = key.split('_')[-1]  # assuming suffixes are defined after the last underscore
        if suffix not in suffix_dict:
            suffix_dict[suffix] = {key: hashmap[key]}
        else:
            suffix_dict[suffix][key] = hashmap[key]
    
    return suffix_dict


def combine_dicts(d:dict):
    combined_dict = {}
    for k, v in d.items():
        if isinstance(v, dict):
            combined_dict.update(v)
        else:
            combined_dict[k] = v
    return combined_dict


def convert_geotimehash(track: Track, precision: int,
     hash_func: Callable):
    """
    Converts a track into a chronnet by a specified timehash precision
    using a specified hashing function
    
    Args:
        track: the target geostructures Track 

        hour_interval: the length in hours of the desired interval

        hash_func: the hashing function


    Returns:
        A geotime hashmap
    """
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