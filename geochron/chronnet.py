import itertools
import networkx as nx
import numpy as np
import pandas as pd

def hash_tracks_into_netdf(track_list , timestamps, hash_func):
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
    master_hashmap = {}
    for track,timestamp  in zip(track_list, timestamps):
        hashmap = hash_func(track)
        start_string= interval_start.strftime("%Y-%m-%d %H:%M:%S")
        end_string= timestamp.strftime("%Y-%m-%d %H:%M:%S")
        interval = start_string + ", " + end_string
        hashmap = {key: interval for key in hashmap}
        interval_start = timestamp
        master_hashmap.update(hashmap)

    df = pd.DataFrame(list(master_hashmap.items()), columns=['cell', 'time'])
    return df



def chronnet_create(df, self_loops= True, mode="directed"):
    time_seq = sorted(np.unique(df['time']))
    if len(time_seq) < 2:
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
    else:
        print("Empty graph returned.")
    return net


