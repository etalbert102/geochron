"Representation as a time grid"
from typing import Callable, List
import math
import pandas as pd
from datetime import  datetime, timedelta
from geostructures.collections import FeatureCollection, Track
from geochron.time_slicing import get_timestamp_intervals, time_slice_track


def break_time_interval(track: Track, time_interval: timedelta):
    timestamps = get_timestamp_intervals(track, time_interval)
    track_list = time_slice_track(track, timestamps)

    return track_list

def round_down_datetime(dt, delta):
    if dt.tzinfo is None:
        min_dt = datetime.min
    else:
        min_dt = datetime.min.replace(tzinfo=dt.tzinfo)
    
    remainder = dt - (dt - min_dt) % delta
    return remainder


def extract_intervals_in_range(start_time, end_time, interval):
    current_time = start_time
    intervals_list = []
    
    while current_time <= end_time:
        intervals_list.append(round_down_datetime(current_time,interval))
        current_time += interval
    
    return intervals_list

def create_time_list_from_datetimes(start_datetime, end_datetime, interval):
    times = []
    current_time = start_datetime
    
    while current_time <= end_datetime:
        times.append(current_time.time())
        current_time += interval
    
    return times




def create_time_grid(track: Track, time_interval: timedelta, time_subinterval: timedelta, hash_func: Callable, integerize = False):
    all_tracks=[]
    num_intervals = math.ceil(time_interval / time_subinterval)
    columns = [f"Period_{i+1}" for i in range(num_intervals)]
    interval_list = extract_intervals_in_range(track.start, track.end, time_interval)
    track_list = break_time_interval(track, time_interval)
    time_list = create_time_list_from_datetimes(interval_list[0],interval_list[1],time_subinterval)
    for tr in track_list:
        interval_tracks= []
        for i in range(len(time_list) - 1): 
            current_time = time_list[i] 
            next_time = time_list[i + 1]
            subinterval_track = tr.filter_by_time(current_time, next_time)
            if len(subinterval_track) > 0 :
                point = subinterval_track.centroid
                hash = list(hash_func.hash_coordinates([point]).keys())[0]
                if integerize is True:
                    interval_tracks.append(int(hash,16))
                else:
                    interval_tracks.append(hash)
            else:
                interval_tracks.append(0)
        all_tracks.append(interval_tracks)
    time_grid = pd.DataFrame(all_tracks, columns=columns)
    time_grid['interval_start'] = interval_list
    return time_grid

