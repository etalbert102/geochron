
import datetime as dt
from geochron.time_slicing import get_timestamp_intervals, time_slice_track
from geostructures import Coordinate, GeoPoint
from geostructures.collections import  Track

track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=dt.datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=dt.datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=dt.datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=dt.datetime(2020, 1, 1, 10, 5)),
    ]
)

def test_get_timestamp_intervals():
    timestamps = get_timestamp_intervals(track,dt.timedelta(hours=1))
    
    assert timestamps[-1] == dt.datetime(2020, 1, 1, 10, 5,1, tzinfo=dt.timezone.utc)



def test_time_slice_track():
    test_timestamps = [dt.datetime(2020, 1, 1, 9, 5, tzinfo=dt.timezone.utc),
    dt.datetime(2020, 1, 1, 10, 5, 1, tzinfo=dt.timezone.utc)]
    track_list = time_slice_track(track, test_timestamps)

    assert track_list[-1].end == dt.datetime(2020, 1, 1, 10, 5, tzinfo=dt.timezone.utc)

    