"Representation as a time grid"
import math
from datetime import  date, datetime, timedelta
from typing import Callable, List
import pandas as pd
from geostructures.collections import FeatureCollection, Track
from geochron.time_slicing import get_timestamp_intervals, time_slice_track
from geostructures.time import TimeInterval


def break_time_interval(track: Track, interval_list: List, time_interval: timedelta):
    """
    Breaks a Track into several tracks partitioned by a time interval.
    
    Args:
        track: The target geostructures Track
        time_interval: A timedelta representing the interval to partition by

    Returns:
        A list of tracks
    """
    timestamps = interval_list.copy()
    timestamps.append(interval_list[-1] + time_interval)
    track_list = time_slice_track(track, timestamps)
    del track_list[0]
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

def extract_intervals_in_range(start_time: datetime, end_time: datetime, interval: timedelta):
    """
    Extracts intervals within a specified range by rounding down to the nearest interval.
    
    Args:
        start_time: A datetime object marking the start of the range.
        end_time: A datetime object marking the end of the range.
        interval: A timedelta object representing the interval to round down to.

    Returns:
        A list of datetime objects representing the intervals rounded 
        down to the nearest specified interval within the range.
    """
    current_time = start_time
    intervals_list = []

    while current_time <= end_time:
        intervals_list.append(round_down_datetime(current_time, interval))
        current_time += interval

    # Add an extra interval to cover the end time if necessary
    if intervals_list[-1] < end_time:
        intervals_list.append(round_down_datetime(current_time, interval))

    return intervals_list




def create_time_list_from_datetimes(start_datetime: datetime, num_intervals: int, interval: timedelta):
    """
    Generates a list of datetime objects from a given start time, creating a specified number of intervals.
    
    Args:
        start_datetime: A datetime object marking the start time.
        num_intervals: The number of intervals to create.
        interval: A timedelta object representing the interval between times.

    Returns:
        A list of datetime objects representing each interval.
    """
    times = []
    current_time = start_datetime

    for _ in range(num_intervals):
        times.append(current_time)
        current_time += interval
    times[-1] = times[-1]- timedelta(seconds=1)
    return times




def convert_time_grid(fcol: FeatureCollection,
                      time_interval: timedelta,
                      time_subinterval: timedelta,
                      hash_func: Callable,
                      integerize=False):
    """
    Converts a track into a time grid dataframe,
    partitioning it by specified time intervals and subintervals.
    
    Args:
        track: The target geostructures Track to be converted.
        time_interval: A timedelta object representing the primary interval to partition the track.
        time_subinterval: A timedelta object representing the subinterval.
        hash_func: A callable function used to hash coordinates of track centroids. Must use hash_coordinates
        integerize: A boolean flag indicating whether to convert hashed values to integers.

    Returns:
        A pandas DataFrame representing the time grid with track segments hashed into intervals (rows) and subintervals (columns).
    """
    all_tracks = []
    track = Track(fcol.geoshapes)
    num_intervals = math.ceil(time_interval / time_subinterval)
    columns = [f"Period_{i+1}" for i in range(num_intervals)]
    interval_list = extract_intervals_in_range(track.start, track.end, time_interval)
    track_list = break_time_interval(track,interval_list, time_interval)

    for tr, interval in zip(track_list, interval_list):
        time_list = create_time_list_from_datetimes(interval, num_intervals+1, time_subinterval)
        interval_tracks = []
        for i in range(len(time_list) - 1):
            current_time = time_list[i] - timedelta(microseconds=1)
            next_time = time_list[i + 1] - timedelta(microseconds=1)
            subinterval_track = tr.filter_by_dt(TimeInterval(current_time,next_time))
            if len(subinterval_track) > 0:
                point = subinterval_track.centroid
                hash_value = list(hash_func([point]).keys())[0]
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
