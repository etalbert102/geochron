""" Representation as a series of trajectories"""
from geochron.time_slicing import get_timestamp_intervals, time_slice_track
from typing import Callable, List
import math
import pandas as pd
from datetime import  datetime, timedelta

def break_time_interval(track: Track, time_interval: timedelta):
    timestamps = get_timestamp_intervals(track, time_interval)
    track_list = time_slice_track(track, timestamps)

    return track_list

def extract_intervals_in_range(start_time, end_time, interval):
    current_time = start_time
    intervals_list = []
    
    while current_time <= end_time:
        intervals_list.append(current_time)
        current_time += interval
    
    # Add an extra interval to cover the end time
    if intervals_list and intervals_list[-1] < end_time:
        intervals_list.append(intervals_list[-1] + interval)
    
    return intervals_list

def create_time_grid(track: Track, time_interval: timedelta):
    total_duration = track.start - track.end
    num_intervals = math.ceil(total_duration / timedelta(days=1))
    columns = [f"Period_{i+1}" for i in range(num_intervals)]


def convert_trajectories(fcol: FeatureCollection, time_interval: timedelta, time_subinterval: timedelta,  hash_func: Callable):
    list_of_lists=[]
    track = Track(fcol)
    track_list = break_time_interval(track, time_interval)

    for tr in track_list:
        subtrack_list = break_time_interval(tr, time_subinterval)
        hash_list = []
        for subtrack in subtrack_list:
            point = subtrack.centroid
            hash = list(hash_func.hash_coordinates([point]).keys())[0]
            hash_list.append(hash)
        hash_list.append(tr.start)
        hash_list.append(tr.end)
        list_of_lists.append(hash_list)
    num_periods = len(hash_list) - 2
    columns = [f"Period_{i+1}" for i in range(num_periods)] + ['start_time', 'end_time']
    df = pd.DataFrame(list_of_lists, columns=columns)