from datetime import datetime, timedelta, timezone
from geochron.geotimehash import precision_delta, generate_times, timehash_geoshape,\
append_timehash_to_geohashmap, breakdown_hashmap_by_suffix, combine_dicts, convert_geotimehash
from geostructures import Coordinate, GeoCircle, GeoPoint
from geostructures.collections import  Track
from geostructures.geohash import H3Hasher
from geostructures.time import  TimeInterval
import pytest 

def test_precision_delta():
    delta1 = precision_delta(1)
    delta2 = precision_delta(2)
    delta3 = precision_delta(3)
    delta4 = precision_delta(4)
    delta5 = precision_delta(5)
    delta6 = precision_delta(6)
    delta7 = precision_delta(7)
    delta8 = precision_delta(8)
    delta9 = precision_delta(9)
    delta10 = precision_delta(10)

    assert delta1 == timedelta(days = 5840)
    assert delta2 == timedelta(days = 730)
    assert delta3 == timedelta(days = 91.2)
    assert delta4 == timedelta(days = 11.4)
    assert delta5 == timedelta(hours = 34.2)
    assert delta6 == timedelta(hours = 4.2)
    assert delta7 == timedelta(minutes = 32)
    assert delta8 == timedelta(minutes = 4)
    assert delta9 == timedelta(seconds = 30)
    assert delta10 == timedelta(seconds = 3.6)
    with pytest.raises(UnboundLocalError):
        precision_delta(11)

def test_generate_times():
    start_time = datetime(2020, 1, 1, 9, 30, tzinfo=timezone.utc)
    end_time = datetime(2020, 1, 1, 9, 42, tzinfo=timezone.utc)
    time_list = generate_times(start_time, end_time, 8)
    time2 = datetime(2020, 1, 1, 9, 38, tzinfo=timezone.utc).timestamp()

    assert time_list[2] == time2

def test_timehash_geoshape():
    circle2 = GeoCircle(
    Coordinate(-0.118092, 51.509865), 
    radius=5000, 
    dt=TimeInterval(datetime(2020, 1, 1, 9, 30), datetime(2020, 1, 1, 9, 42))
    )
    timehash_list = timehash_geoshape(circle2, 8)

    assert timehash_list[2] == 'b0ffffbc'

def test_append_timehash_to_geohashmap():
    geohashmap = {'8b194ad32161fff': 1.0,
                '8b194ad32b23fff': 1.0,
                '8b194ad32b1dfff': 1.0,
                '8b194ad32b33fff': 1.0}
    
    timehash_list = ['b0ffffbc']

    geotime_map = append_timehash_to_geohashmap(geohashmap, timehash_list)

    assert geotime_map['8b194ad32161fff_b0ffffbc'] == 1

def test_breakdown_hashmap_by_suffix():
    hashmap = {'8b194ad32161fff_b0ffffbc': 1.0,
                '8b194ad32b23fff_b0ffffbc': 1.0,
                '8b194ad32b1dfff_b0ffffba': 1.0,
                '8b194ad32b33fff_b0ffffba': 1.0}
    
    dict_of_dicts = breakdown_hashmap_by_suffix(hashmap)

    assert dict_of_dicts['b0ffffbc']['8b194ad32b23fff_b0ffffbc'] == 1

def test_combine_dicts():
    # Test with a dictionary of dictionaries
    d = {'dict1': {'key1': 'value1', 'key2': 'value2'}, 'dict2': {'key3': 'value3', 'key4': 'value4'}}
    combined = combine_dicts(d)
    assert combined == {'key1': 'value1', 'key2': 'value2', 'key3': 'value3', 'key4': 'value4'}

    # Test with a dictionary containing non-dictionary items
    d = {'dict1': {'key1': 'value1', 'key2': 'value2'}, 'non_dict': 'value'}
    combined = combine_dicts(d)
    assert combined == {'key1': 'value1', 'key2': 'value2', 'non_dict': 'value'}
              
def test_convert_geotimehash():
    hasher = H3Hasher(resolution = 10)
    track = Track(
    [
        GeoPoint(Coordinate(-0.104154, 51.511920), dt=datetime(2020, 1, 1, 8, 5)),
        GeoPoint(Coordinate(-0.096533, 51.511903), dt=datetime(2020, 1, 1, 9, 23)),
        GeoPoint(Coordinate(-0.083765, 51.514423), dt=datetime(2020, 1, 1, 9, 44)),
        GeoPoint(Coordinate(-0.087478, 51.508595), dt=datetime(2020, 1, 1, 10, 5)),
    ]
    )

    geotimehash = convert_geotimehash(track, 8, hasher.hash_collection)

    assert geotimehash['8a194ad3056ffff_b0ffffbe'] == 1

    
    