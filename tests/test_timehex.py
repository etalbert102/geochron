import datetime as dt
from geochron.timehex import hash_tracks_into_timehexdf, convert_timehex
from geostructures import Coordinate, GeoPoint
from geostructures.collections import  Track
from geostructures.geohash import H3Hasher

hasher = H3Hasher(resolution = 10)
test_timestamps = [dt.datetime(2020, 1, 1, 9, 5, tzinfo=dt.timezone.utc),
dt.datetime(2020, 1, 1, 10, 5, 1, tzinfo=dt.timezone.utc)]

def test_hash_tracks_into_timehexdf():

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
    test_df = hash_tracks_into_timehexdf(track_list, test_timestamps, hasher.hash_collection)

    assert test_df['8a194ad3056ffff'].values[1] == 1


def test_convert_chronnet():
    track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
    )

    test_timehex = convert_timehex(track, dt.timedelta(hours=1), hasher.hash_collection)

    assert test_timehex['8a194ad3056ffff'].values[1] == 1