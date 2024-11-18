import pytest
import pandas as pd
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
    interval_list = [
        datetime(2020, 1, 1, 8, 0),
        datetime(2020, 1, 1, 9, 0),
        datetime(2020, 1, 1, 10, 0),
    ]
    
    result = break_time_interval(sample_track, interval_list, time_interval)
    
    # Check the length of the result
    assert len(result) == 3
    

    assert result[0] == Track([GeoPoint(Coordinate(-0.104154, 51.511920), dt=datetime(2020, 1, 1, 8, 5))])
    
    # Ensure the end times are handled correctly
    assert result[2] == Track([GeoPoint(Coordinate(-0.087478, 51.508595), dt=datetime(2020, 1, 1, 10, 11))])


def test_round_down_datetime():
    # Test cases
    test_cases = [
        (datetime(2023, 1, 1, 8, 5), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 59), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 30), timedelta(minutes=15), datetime(2023, 1, 1, 8, 30)),
        (datetime(2023, 1, 1, 8, 45), timedelta(minutes=30), datetime(2023, 1, 1, 8, 30)),
        (datetime(2023, 1, 1, 8, 0, tzinfo=None), timedelta(hours=1), datetime(2023, 1, 1, 8, 0)),
        (datetime(2023, 1, 1, 8, 0), timedelta(days=1), datetime(2023, 1, 1, 0, 0)),
        (pd.Timestamp(datetime(2023, 1, 1, 8, 0)), timedelta(days=1), datetime(2023, 1, 1, 0, 0))
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
    start_datetime = datetime(2023, 1, 1, 0, 0, 0)
    num_intervals = 5
    interval = timedelta(hours=1)
    
    expected_times = [
        datetime(2023, 1, 1, 0, 0, 0),
        datetime(2023, 1, 1, 1, 0, 0),
        datetime(2023, 1, 1, 2, 0, 0),
        datetime(2023, 1, 1, 3, 0, 0),
        datetime(2023, 1, 1, 3, 59, 59)  # Adjusted by subtracting one second
    ]
    
    result = create_time_list_from_datetimes(start_datetime, num_intervals, interval)
    
    assert result == expected_times

# Mock hash function for testing
class MockHashFunc:
    def hash_coordinates(self, points):
        return {f"hash_{i}": point for i, point in enumerate(points)}

def test_convert_time_grid(sample_track):
    time_interval = timedelta(hours=1)
    time_subinterval = timedelta(minutes=30)
    hash_func = MockHashFunc()
    result = convert_time_grid(sample_track, time_interval, time_subinterval, hash_func.hash_coordinates)

    # Expected DataFrame structure
    expected_columns = ['Period_1', 'Period_2', 'interval_start']
    assert list(result.columns) == expected_columns
    assert result['Period_1'][0] == 'hash_0'
    assert result['Period_2'][0] == 0 



