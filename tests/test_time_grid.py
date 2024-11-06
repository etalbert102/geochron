import pytest
import math
from datetime import datetime, timedelta

from geostructures import Coordinate, GeoPoint
from geostructures.collections import  Track

from geochron.time_grid import  break_time_interval, round_down_datetime, extract_intervals_in_range \
,create_time_list_from_datetimes, convert_time_grid 

@pytest.fixture
def sample_track():
    return Track(
        [
            GeoPoint(Coordinate(-0.104154, 51.511920), dt=datetime(2020, 1, 1, 8, 5)),
            GeoPoint(Coordinate(-0.096533, 51.511903), dt=datetime(2020, 1, 1, 9, 23)),
            GeoPoint(Coordinate(-0.083765, 51.514423), dt=datetime(2020, 1, 1, 9, 44)),
            GeoPoint(Coordinate(-0.087478, 51.508595), dt=datetime(2020, 1, 1, 10, 11)),
        ]
    )


def test_break_time_interval(sample_track):
    time_interval = timedelta(hours=1)
    broken_tracks = break_time_interval(sample_track, time_interval)

    # Validate the number of returned tracks
    assert len(broken_tracks) == 3  # Assuming the intervals cover the given points

    # Validate the contents of each track
    assert len(broken_tracks[0]) == 1  # First interval: One GeoPoint
    assert broken_tracks[0].geoshapes[0].coordinate == Coordinate(-0.104154, 51.511920)

    assert len(broken_tracks[1]) == 2  # Second interval: Two GeoPoints
    assert broken_tracks[1].geoshapes[0].coordinate == Coordinate(-0.096533, 51.511903)
    assert broken_tracks[1].geoshapes[1].coordinate == Coordinate(-0.083765, 51.514423)


    assert len(broken_tracks[2]) == 1  # Third interval: One GeoPoint
    assert broken_tracks[2].geoshapes[0].coordinate == Coordinate(-0.087478, 51.508595)


def test_round_down_datetime():
    # Test cases
    test_cases = [
        (datetime(2023, 1, 1, 8, 5), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 59), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 30), timedelta(minutes=15), datetime(2023, 1, 1, 8, 30)),
        (datetime(2023, 1, 1, 8, 45), timedelta(minutes=30), datetime(2023, 1, 1, 8, 30)),
        (datetime(2023, 1, 1, 8, 0, tzinfo=None), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 0), timedelta(days=1), datetime(2023, 1, 1, 0, 0)),
    ]
    
    for dt, delta, expected in test_cases:
        assert round_down_datetime(dt, delta) == expected

def test_extract_intervals_in_range():
    # Define test cases
    start_time = datetime(2023, 1, 1, 0, 0, 0)
    end_time = datetime(2023, 1, 1, 6, 0, 0)
    interval = timedelta(hours=2)
    
    expected_intervals = [
        datetime(2023, 1, 1, 0, 0, 0),
        datetime(2023, 1, 1, 2, 0, 0),
        datetime(2023, 1, 1, 4, 0, 0),
        datetime(2023, 1, 1, 6, 0, 0)
    ]

    # Execute the function
    result_intervals = extract_intervals_in_range(start_time, end_time, interval)

    # Check that the results match the expected intervals
    assert result_intervals == expected_intervals

def test_create_time_list_from_datetimes():
    # Define test case
    start_datetime = datetime(2023, 1, 1, 6, 0, 0)
    end_datetime = datetime(2023, 1, 1, 10, 0, 0)
    interval = timedelta(hours=1)
    
    expected_times = [
        datetime(2023, 1, 1, 6, 0, 0).time(),
        datetime(2023, 1, 1, 7, 0, 0).time(),
        datetime(2023, 1, 1, 8, 0, 0).time(),
        datetime(2023, 1, 1, 9, 0, 0).time(),
        datetime(2023, 1, 1, 10, 0, 0).time(),
    ]
    
    result_times = create_time_list_from_datetimes(start_datetime, end_datetime, interval)
    
    assert result_times == expected_times

class MockHasher:
    def hash_coordinates(self, points):
        return {str(point): "hashed_value" for point in points}

def test_convert_time_grid(sample_track):
    time_interval = timedelta(hours=2)
    time_subinterval = timedelta(hours=1)
    mock_hash_func = MockHasher()

    result_df = convert_time_grid(sample_track, time_interval, time_subinterval, mock_hash_func)

    # Define expected columns
    num_intervals = math.ceil(time_interval / time_subinterval)
    expected_columns = [f"Period_{i+1}" for i in range(num_intervals)]
    expected_columns.append('interval_start')

    # Check if the DataFrame has the correct columns
    assert list(result_df.columns) == expected_columns

    # Check if the DataFrame has the expected number of rows
    assert len(result_df) == 2

    # Validate the DataFrame content
    for idx, row in result_df.iterrows():
        assert row['Period_1'] == "hashed_value" or row['Period_1'] == 0


