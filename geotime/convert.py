""" Conversion from FeatureCollection to geotime datastructure """
from typing import String
from geostructures.collection import  FeatureCollection, Track
from geotime.chronnet import chronnet_create
from geotime.timecube import TimeCube
from datetime import datetime, timedelta

def time_slice_track(track: Track, hour_interval: int):
    """
    Slices a Track into several tracks that are partitioned by a specified length
    of time in hours  
    
    Args:
        track: the target Track

        hour_interval= the length in hours of the desired interval

    Returns:
        A list of sliced tracks
    """
    start_time = track.start
    end_time = track.end
    timestamps = []
    sliced_tracks = []

    # get timestamp intervals
    date_x = start_time
    while date_x < end_time:
        date_x += timedelta(hours = hour_interval)
        timestamps.append(date_x)
    
    
    for timestamp in timestamps:
        sliced_track = track[start_time: timestamp]
        start_time = timestamp
        sliced_tracks.append(sliced_track)
    
    return sliced_tracks

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

    if datastructure == "timecube":
        result = 
    elif datastructure == "chronnet":
        result = 
    else:
        print("Data structure not currently supported please check doc string for supported options")

    return result