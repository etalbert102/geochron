""" Functions needed to slice tracks by time"""
from datetime import  timedelta
from typing import List
from geostructures.collections import  Track



def get_timestamp_intervals(track: Track, time_delta: timedelta):
    """
    gets the timestamps for a Track partitioned by a specified length
    of time in hours  
    
    Args:
        track: the target geostructures Track

        time_delta: the desired time interval

    Returns:
        A list of timestamps starting from an interval from the start
    """
    start_time = track.start
    end_time = track.end
    timestamps = []

    # get timestamp intervals
    date_x = start_time
    while date_x < end_time:
        date_x += time_delta
        timestamps.append(date_x)

    # change the last value to be inclusive
    timestamps[-1] = timestamps[-1] + timedelta(seconds=1)


    return timestamps


def time_slice_track(track: Track, timestamps: List):
    """
    Slices a Track into several tracks that are partitioned by a list
    of time stamps  
    
    Args:
        track: the target geostructures Track

        timestamps= a list of timestamps

    Returns:
        A list of tracks
    """
    start_time = track.start
    sliced_tracks = []


    for timestamp in timestamps:
        sliced_track = track[start_time: timestamp]
        start_time = timestamp
        sliced_tracks.append(sliced_track)

    return sliced_tracks
