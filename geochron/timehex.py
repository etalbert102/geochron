""" Representation as time hexes """
from datetime import  timedelta
from typing import Callable, List
import pandas as pd
from geostructures.collections import FeatureCollection, Track
from geochron.time_slicing import get_timestamp_intervals, time_slice_track





def hash_tracks_into_timehexdf(track_list: List, timestamps: List, hash_func: Callable):
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

    split_df = df['interval'].str.split(',', expand=True)# pylint: disable=unsubscriptable-object
    df.loc[:, 'start_time'] = pd.to_datetime(split_df[0])
    df.loc[:, 'end_time'] = pd.to_datetime(split_df[1])

    return df

def convert_timehex(fcol: FeatureCollection, time_delta: timedelta, hash_func: Callable):
    """
    Converts a FeatureCollection into a timehex representation with a specified time interval
    using a specified hashing function
    
    Args:
        fcol: a FeatureCollection with time bound shapes

        time_delta: the desired time interval

        hash_func: the hashing function

    Returns:
        A pandas dataframe
    """
    track = Track(fcol.geoshapes)

    timestamps = get_timestamp_intervals(track, time_delta)

    track_list = time_slice_track(track, timestamps)

    timehex_df = hash_tracks_into_timehexdf(track_list, timestamps, hash_func)


    return timehex_df
