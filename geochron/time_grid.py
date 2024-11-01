"Representation as a time grid"
from typing import Callable, List
import math
import pandas as pd
from datetime import  datetime, timedelta
from geostructures.collections import FeatureCollection, Track
from geochron.time_slicing import get_timestamp_intervals, time_slice_track


def break_time_interval(track: Track, time_interval: timedelta):
    """
    Breaks a Track into several tracks partitioned by a time interval.
    
    Args:
        track: The target geostructures Track
        time_interval: A timedelta representing the interval to partition by

    Returns:
        A list of tracks
    """
    timestamps = get_timestamp_intervals(track, time_interval)
    track_list = time_slice_track(track, timestamps)

    return track_list


def round_down_datetime(dt:datetime, delta:timedelta):
    """
    Rounds down a datetime object to the nearest interval of the specified timedelta.
    
    Args:
        dt: The datetime object to be rounded down.
        delta: A timedelta object representing the interval to round down to.

    Returns:
        A datetime object rounded down to the nearest interval of the specified timedelta.
    """
    if dt.tzinfo is None:
        min_dt = datetime.min
    else:
        min_dt = datetime.min.replace(tzinfo=dt.tzinfo)
    
    remainder = dt - (dt - min_dt) % delta
    return remainder


def extract_intervals_in_range(start_time:datetime, end_time:datetime, interval:timedelta):
    """
    Extracts intervals within a specified range by rounding down to the nearest interval.
    
    Args:
        start_time: A datetime object marking the start of the range.
        end_time: A datetime object marking the end of the range.
        interval: A timedelta object representing the interval to round down to.

    Returns:
        A list of datetime objects representing the intervals rounded down to the nearest specified interval within the range.
    """
    current_time = start_time
    intervals_list = []
    
    while current_time <= end_time:
        intervals_list.append(round_down_datetime(current_time, interval))
        current_time += interval
    
    return intervals_list

def create_time_list_from_datetimes(start_datetime:datetime, end_datetime:datetime, interval:timedelta):
    """
    Generates a list of time objects from datetime intervals within a specified range.
    
    Args:
        start_datetime: A datetime object marking the start of the range.
        end_datetime: A datetime object marking the end of the range.
        interval: A timedelta object representing the interval between times.

    Returns:
        A list of time objects representing each interval within the range.
    """
    times = []
    current_time = start_datetime
    
    while current_time <= end_datetime:
        times.append(current_time.time())
        current_time += interval
    
    return times


def convert_time_grid(track: Track, time_interval: timedelta, time_subinterval: timedelta, hash_func: Callable, integerize=False):
    """
    Converts a track into a time grid dataframe, partitioning it by specified time intervals and subintervals.
    
    Args:
        track: The target geostructures Track to be converted.
        time_interval: A timedelta object representing the primary interval to partition the track.
        time_subinterval: A timedelta object representing the subinterval for detailed slicing within each primary interval.
        hash_func: A callable function used to hash coordinates of track centroids.
        integerize: A boolean flag indicating whether to convert hashed values to integers (default is False).

    Returns:
        A pandas DataFrame representing the time grid with track segments hashed into intervals and subintervals.
    """
    all_tracks = []
    num_intervals = math.ceil(time_interval / time_subinterval)
    columns = [f"Period_{i+1}" for i in range(num_intervals)]
    interval_list = extract_intervals_in_range(track.start, track.end, time_interval)
    track_list = break_time_interval(track, time_interval)
    time_list = create_time_list_from_datetimes(interval_list[0], interval_list[1], time_subinterval)
    
    for tr in track_list:
        interval_tracks = []
        for i in range(len(time_list) - 1): 
            current_time = time_list[i] 
            next_time = time_list[i + 1]
            subinterval_track = tr.filter_by_time(current_time, next_time)
            if len(subinterval_track) > 0:
                point = subinterval_track.centroid
                hash_value = list(hash_func.hash_coordinates([point]).keys())[0]
                if integerize:
                    interval_tracks.append(int(hash_value, 16))
                else:
                    interval_tracks.append(hash_value)
            else:
                interval_tracks.append(0)
        all_tracks.append(interval_tracks)
    
    time_grid = pd.DataFrame(all_tracks, columns=columns)
    time_grid['interval_start'] = interval_list
    return time_grid


