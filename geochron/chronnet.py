import itertools
import networkx as nx
import numpy as np
import pandas as pd
from geostructures.collections import  Track
from typing import Callable, List
from geochron.time_slicing import get_timestamp_intervals, time_slice_track 

def hash_tracks_into_netdf(track_list: List, timestamps: List, hash_func: Callable):
    """
    Converts a list of tracks into a pandas dataframe suitable for chron net creation
    using a specified hashing function with intervals reflected
    in a corresponding timestamp list 
    
    Args:
        track_list: a list of tracks broken down by equal intervals

        timestamps: a list of corresponding timestamps

        hash_func: the hashing function

    Returns:
        A pandas dataframe
    """
    interval_start = track_list[0].start
    master_list = []
    for track,timestamp  in zip(track_list, timestamps):
        hashmap = hash_func(track)
        start_string= interval_start.strftime("%Y-%m-%d %H:%M:%S")
        end_string= timestamp.strftime("%Y-%m-%d %H:%M:%S")
        interval = start_string + ", " + end_string
        hexes = list(hashmap.keys())
        counts = list(hashmap.values())
        hex_list = [element for element, count in zip(hexes, counts) for _ in range(count)]
        tuples_list = [(item, interval) for item in hex_list]
        master_list += tuples_list
        interval_start = timestamp
        

    df = pd.DataFrame(master_list, columns=['cell', 'time'])
    
    return df


def chronnet_create(df: pd.DataFrame, self_loops: bool, mode= str):
    """
    Converts a properly formatted pandas dataframe with the columns
    of cell and time to a networkx network. 
    
    Args:
        df: a pandas dataframe withe two columns cell and time

        self_loops: whether self loops are included in the network

        mode: whether the network is directed or undirected

    Returns:
        A networkx network
    """
    time_seq = sorted(np.unique(df['time']))
    if len(time_seq) < 2: # pragma: no cover
        print("The total time interval in the dataset should be larger than two.")
    links = pd.DataFrame()
    cells_before=[]
    cells_after=[]
    weights = []
    for i in range(len(time_seq)-1):
        time1 = df[df.time == time_seq[i]]['cell'].tolist()
        time2 = df[df.time == time_seq[i+1]]['cell'].tolist()
        connections = list(itertools.product(time1, time2))
        cells_before.extend([connection[0] for connection in connections])
        cells_after.extend([connection[1] for connection in connections])
        weights.extend([1]*len(connections))
    links['from'] = cells_before
    links['to'] = cells_after
    links['weight'] = weights
    links = links.sort_values(by=['from', 'to']).reset_index().drop(columns = ['index'])
    links = links.groupby(['from', 'to'], as_index=False)['weight'].sum()
    net = nx.DiGraph()
    if len(links) !=0:
        net.add_nodes_from(np.unique(df['cell']))
        edgelist = []
        for index, rows in links.iterrows():
            edgelist.append(tuple([rows['from'], rows['to'], rows['weight']]))
        net.add_weighted_edges_from(edgelist)
        if self_loops == False:
            net.remove_edges_from(list(nx.selfloop_edges(net)))
        if mode == 'undirected':
            net = net.to_undirected()
    else: # pragma: no cover
        print("Empty graph returned.")
    
    return net


def convert_chronnet(track: Track, hour_interval: float,
     hash_func: Callable, self_loops: bool, mode: str):
    """
    Converts a track into a chronnet with a specified time interval
    using a specified hashing function
    
    Args:
        track: the target geostructures Track 

        hour_interval: the length in hours of the desired interval

        hash_func: the hashing function

        self_loops: whether self loops are included in the network

        mode: whether the network is directed or undirected

    Returns:
        A networkx network 
    """
    timestamps = get_timestamp_intervals(track, hour_interval)

    track_list = time_slice_track(track, timestamps)

    df = hash_tracks_into_netdf(track_list, timestamps, hash_func)

    chronnet = chronnet_create(df, self_loops, mode)

    return chronnet 