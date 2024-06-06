""" Representation as geosynchnet"""
from datetime import  timedelta
from typing import Callable
import pandas as pd

from geostructures.collections import  FeatureCollection,Track
from geochron.chronnet import hash_tracks_into_netdf
from geochron.time_slicing import get_timestamp_intervals, time_slice_track

def geosynchnet_create(df: pd.DataFrame):
    """
    Converts a properly formatted pandas dataframe with the columns
    of cell and time to a networkx network where nodes are locations
    and edges are formed between nodes with that share a time. 
    
    Args:
        df: a pandas dataframe withe two columns cell and time

    Returns:
        A networkx network
    """
    import networkx as nx
    net = nx.Graph()

    grouped = df.groupby('time')

    for name, group in grouped:
        cells = group['cell'].tolist()
        for i, cell_i in enumerate(cells):
            for cell_j in cells[i+1:]:
                if net.has_edge(cell_i, cell_j):
                    # if the edge already exists, increment the weight by 1
                    net[cell_i][cell_j]['weight'] += 1
                else:
                    # otherwise, add the edge with a weight of 1
                    net.add_edge(cell_i, cell_j, weight=1)

    return net


def convert_geosynchnet(fcol: FeatureCollection, time_delta: timedelta,
     hash_func: Callable):
    """
    Converts a FeatureCollection into a chronnet with a specified time interval
    using a specified hashing function
    
    Args:
        fcol: a FeatureCollection with time bound shapes 

        time_delta: the desired time interval

        hash_func: the hashing function

    Returns:
        A networkx network 
    """
    track = Track(fcol.geoshapes)
    timestamps = get_timestamp_intervals(track, time_delta)

    track_list = time_slice_track(track, timestamps)

    df = hash_tracks_into_netdf(track_list, timestamps, hash_func)

    geosynchnet = geosynchnet_create(df)

    return geosynchnet
