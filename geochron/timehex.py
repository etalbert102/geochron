""" Representation as time hexes """
from geostructures.collections import Track
from datetime import  timedelta
from geostructures.geohash import H3Hasher
import pandas as pd

def get_timestamp_intervals(track: Track, hour_interval: int):
    """
    gets the timestamps for a Track partitioned by a specified length
    of time in hours  
    
    Args:
        track: the target Track

        hour_interval= the length in hours of the desired interval

    Returns:
        A list of timestamps starting from an interval from the start
    """
    start_time = track.start
    end_time = track.end
    timestamps = []

    # get timestamp intervals
    date_x = start_time
    while date_x < end_time:
        date_x += timedelta(hours = hour_interval)
        timestamps.append(date_x)
    
    # change the last value to be inclusive 
    timestamps[-1] = timestamps[-1] + timedelta(seconds=1)
    
    
    return timestamps


def time_slice_track(track: Track, timestamps):
    """
    Slices a Track into several tracks that are partitioned by a list
    of time stamps  
    
    Args:
        track: the target Track

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


def hash_tracks_into_df(track_list , timestamps, hash_func):
    """
    Converts a list of tracks into a pandas dataframe using
    a specified hashing function with intervals reflected
    in a corresponding timestamp list 
    
    Args:
        track_list: a list of tracks broken down by equal intervals

        timestamps: a list of corresponding timestamps

        hash_func: the hashing function

    Returns:
        A pandas dataframe
    """
    interval_start = track_list[0].start
    row_list = []
    for track,timestamp  in zip(track_list, timestamps):
        hashmap = hash_func(track)
        start_string= interval_start.strftime("%Y-%m-%d %H:%M:%S")
        end_string= timestamp.strftime("%Y-%m-%d %H:%M:%S")
        interval = start_string + ", " + end_string
        new_row = pd.Series(data=hashmap, name=interval)
        row_list.append(new_row)
        interval_start = timestamp
    
    df = pd.DataFrame(row_list)
    
    df = df.reset_index(names='interval')

    df[['start_time', 'end_time']] = df['interval'].str.split(',', expand=True)
    
    return df