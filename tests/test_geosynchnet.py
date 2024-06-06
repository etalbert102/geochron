import datetime as dt
import pandas as pd
from geochron.geosynchnet import geosynchnet_create, convert_geosynchnet
from geostructures import Coordinate, GeoPoint
from geostructures.collections import  Track
from geostructures.geohash import H3Hasher

hasher = H3Hasher(resolution = 10)

def test_geosynchnet_create():
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
    test_network = geosynchnet_create(test_df)

    assert list(test_network)[0] == '8a194ad32b07fff'
    assert test_network.has_edge('8a194ad32b07fff', '8a194ad3056ffff') == True
    assert test_network.has_edge('8a194ad32167fff', '8a194ad3078ffff') == False
    assert test_network['8a194ad32b07fff']['8a194ad3056ffff']['weight'] == 1

def test_convert_geosynchnet():
    track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )

    test_geosynchnet = convert_geosynchnet(track, dt.timedelta(hours=1), hasher.hash_collection)
    
    assert list(test_geosynchnet)[0] == '8a194ad32b07fff'
    assert test_geosynchnet.has_edge('8a194ad32b07fff', '8a194ad3056ffff') == True