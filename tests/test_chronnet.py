import datetime as dt
import networkx as nx
import pandas as pd
from geochron.chronnet import hash_tracks_into_netdf, chronnet_create, convert_chronnet
from geostructures import Coordinate, GeoPoint
from geostructures.collections import  Track
from geostructures.geohash import H3Hasher

hasher = H3Hasher(resolution = 10)
test_timestamps = [dt.datetime(2020, 1, 1, 9, 5, tzinfo=dt.timezone.utc),
dt.datetime(2020, 1, 1, 10, 5, 1, tzinfo=dt.timezone.utc)]

def test_hash_tracks_into_netdf():

    track1 = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5))
    ]
    )
    track2 = Track(
    [
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )

    track_list = [track1, track2]
    test_df = hash_tracks_into_netdf(track_list, test_timestamps, hasher.hash_collection)

    assert test_df['cell'].values[4] == '8a194ad3078ffff'

def test_chronnet_create():
    test_dict={'cell': {0: '8a194ad32167fff',
    1: '8a194ad32b07fff',
    2: '8a194ad3056ffff',
    3: '8a194ad3078ffff',
    4: '8a194ad3078ffff'},
    'time': {0: '2020-01-01 08:05:00, 2020-01-01 09:05:00',
    1: '2020-01-01 09:05:00, 2020-01-01 10:05:01',
    2: '2020-01-01 09:05:00, 2020-01-01 10:05:01',
    3: '2020-01-01 09:05:00, 2020-01-01 10:05:01',
    4: '2020-01-01 10:05:01, 2020-01-01 11:05:01',}}

    test_df = pd.DataFrame(test_dict)

    test_network = chronnet_create(test_df, True, "directed")
    test_network_ud = chronnet_create(test_df, True, "undirected")
    no_self_loop = chronnet_create(test_df, False, "directed")

    assert list(test_network)[0] == '8a194ad3056ffff'
    assert test_network_ud.is_directed() == False
    assert list(nx.selfloop_edges(test_network )) == [('8a194ad3078ffff', '8a194ad3078ffff')]
    assert list(nx.selfloop_edges(no_self_loop)) == []

def test_convert_chronnet():
    track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )

    test_chronnet = convert_chronnet(track, dt.timedelta(hours=1), hasher.hash_collection, True, "directed")
    
    assert list(test_chronnet)[0] == '8a194ad3056ffff'
    
