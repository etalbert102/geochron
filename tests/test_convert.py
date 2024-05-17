import datetime as dt
from geochron import convert
from geostructures import Coordinate, GeoPoint
from geostructures.collections import  FeatureCollection

def test_convert():
    featurecollection = FeatureCollection(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )
    test_chronnet = convert(featurecollection,"chronnet", 1)
    test_timehex = convert(featurecollection,"timehex", 1)
    test_geotimehash = convert(featurecollection,"geotimehash", 1, precision=8)


    assert list(test_chronnet)[0] == '8a194ad3056ffff'
    assert test_timehex['8a194ad3056ffff'].values[1] == 1
    assert test_geotimehash['8a194ad3056ffff_b0ffffbe'] == 1



