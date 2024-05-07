import datetime as dt
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
    ]
    )

    track_list = [track1, track2]
    test_df = hash_tracks_into_netdf(track_list, test_timestamps, hasher.hash_collection)

    assert test_df['cell'].values[2] == '8a194ad3056ffff'

def test_chronnet_create():
    test_dict={'cell': {0: '8a194ad32167fff',
    1: '8a194ad32b07fff',
    2: '8a194ad3056ffff',
    3: '8a194ad3078ffff'},
    'time': {0: '2020-01-01 08:05:00, 2020-01-01 09:05:00',
    1: '2020-01-01 09:05:00, 2020-01-01 10:05:01',
    2: '2020-01-01 09:05:00, 2020-01-01 10:05:01',
    3: '2020-01-01 09:05:00, 2020-01-01 10:05:01'}}

    test_df = pd.DataFrame(test_dict)

    test_network = chronnet_create(test_df)

    assert list(test_network)[0] == '8a194ad3056ffff'

def test_convert_chronnet():
    track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )

    test_chronnet = convert_chronnet(track, 1, hasher.hash_collection)

    assert list(test_chronnet)[0] == '8a194ad3056ffff'
