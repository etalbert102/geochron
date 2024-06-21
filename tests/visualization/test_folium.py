import json
import pandas as pd
import h3
import pytest
from branca.colormap import LinearColormap
from geochron.visualization.folium import *

def test_timehex_styledict():
    # Create a sample dataframe for testing
    data = {
        'start_time': pd.date_range(start='1/1/2022', periods=3),
        'interval': [1, 2, 3],
        'end_time': pd.date_range(start='1/4/2022', periods=3),
        'hex1': [1, 2, 3],
        'hex2': [4, 5, 6],
        'hex3': [7, 8, 9]
    }
    df = pd.DataFrame(data)

    # Call the function with the test dataframe
    result = timehex_styledict(df)
    result_color_list = timehex_styledict(df,opacity=.5 ,cmap = ['blue','yellow'])
    result_colors = timehex_styledict(df , cmap = LinearColormap(colors=['blue','yellow'], vmin=0, vmax=100))
    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys and values
    for key in ['hex1', 'hex2', 'hex3']:
        assert key in result
        assert isinstance(result[key], dict)
        for time_key in result[key]:
            assert 'color' in result[key][time_key]
            assert 'opacity' in result[key][time_key]
    assert result_color_list['hex1'][1640995200] == {'color': '#0000ffff', 'opacity': 0.5}
    assert result_colors['hex1'][1640995200] == {'color': '#0202fdff', 'opacity': 0.7}

    


def test_h3_to_geojson():
    # Define a sample H3 hashmap
    h3_hashmap = {
        "89283082837ffff": {"property1": "value1"},
        "89283082833ffff": {"property2": "value2"}
    }

    # Call the function with the sample H3 hashmap
    result = h3_to_geojson(h3_hashmap)

    # Parse the result as JSON
    result_json = json.loads(result)

    # Check if the result is a FeatureCollection
    assert result_json["type"] == "FeatureCollection"

    # Check if the FeatureCollection contains the correct number of features
    assert len(result_json["features"]) == len(h3_hashmap)

    # Check if each feature in the FeatureCollection is correctly formed
    for feature in result_json["features"]:
        assert feature["type"] == "Feature"
        assert "geometry" in feature
        assert "properties" in feature
        assert "id" in feature
        assert feature["geometry"]["type"] == "Polygon"
        assert len(feature["geometry"]["coordinates"]) > 0
        assert feature["id"] in h3_hashmap
        assert feature["properties"] == h3_hashmap[feature["id"]]

def test_timehex_backgroundata():
    # Define a sample timehex dataframe
    data = {
        "interval": [1, 2],
        "start_time": ["2020-01-01", "2020-02-01"],
        "end_time": ["2020-01-31", "2020-02-29"],
        "89283082837ffff": [{"property1": "value1"}, {"property2": "value2"}],
        "89283082833ffff": [{"property3": "value3"}, {"property4": "value4"}]
    }
    timehex = pd.DataFrame(data)

    # Call the function with the sample timehex dataframe
    result = timehex_backgroundata(timehex)

    # Parse the result as JSON
    result_json = json.loads(result)

    # Check if the result is a FeatureCollection
    assert result_json["type"] == "FeatureCollection"

    # Check if the FeatureCollection contains the correct number of features
    assert len(result_json["features"]) == len(timehex.columns) - 3

    # Check if each feature in the FeatureCollection is correctly formed
    for feature in result_json["features"]:
        assert feature["type"] == "Feature"
        assert "geometry" in feature
        assert "properties" in feature
        assert "id" in feature
        assert feature["geometry"]["type"] == "Polygon"
        assert len(feature["geometry"]["coordinates"]) > 0
        assert feature["id"] in timehex.columns

def test_normalize():
    # Test case 1: Normalization with min_val = 0 and max_val = 1
    assert normalize(0.5, 0, 1) == 0.5

    # Test case 2: Normalization with min_val = -1 and max_val = 1
    assert normalize(0, -1, 1) == 0.5

    # Test case 3: Normalization with min_val = 10 and max_val = 20
    assert normalize(15, 10, 20) == 0.5

    with pytest.raises(ValueError):
        normalize(0, 0, 0)

def test_constant_return():
    # Test case 1: Value doesn't matter; constant should always be returned
    assert constant_return(42, 5) == 5

    # Test case 2: Another arbitrary value and constant
    assert constant_return(0, -10) == -10


def test_add_hashmap_properties():
    # Define a simple colormap function for testing
    def cmap(value):
        return '#000000'

    # Define the original hashmap
    original_hashmap = {'89283082837ffff': 1, '89283082833ffff': 0}
    time = '2024-06-05'
    opacity = 0.7

    # Call the function with the test inputs
    result = add_hashmap_properties(original_hashmap, time, opacity, cmap)
    result_color_list = add_hashmap_properties(original_hashmap, time, opacity, cmap = ['blue','yellow'])
    # Define the expected result
    expected_result = {
        '89283082837ffff': {
            'popup': 'weight= 1<br> center(lat,lon)= ' + str(h3.h3_to_geo('89283082837ffff')),
            'time': time,
            'style': {'opacity': opacity, 'color': cmap(1), 'fillOpacity': opacity}
        }
    }

    expected_result_color_list = {
        '89283082837ffff': {
            'popup': 'weight= 1<br> center(lat,lon)= ' + str(h3.h3_to_geo('89283082837ffff')),
            'time': time,
            'style': {'opacity': opacity, 'color': '#0000ffff', 'fillOpacity': opacity}
        }
    }

    # Assert that the function output is as expected
    assert result == expected_result
    assert result_color_list == expected_result_color_list

def test_timehex_timestampedgeojson():
    # Prepare a sample dataframe
    data = {
        'start_time': ['2022-01-01', '2022-01-02'],
        'interval': [1, 1],
        'end_time': ['2022-01-02', '2022-01-03'],
        '89283082837ffff': [1, 2],
        '89283082833ffff': [3, 4]
    }
    df = pd.DataFrame(data)

    # Call the function with the sample dataframe and colormap
    result = timehex_timestampedgeojson(df)

    assert isinstance(result, dict)
    assert result['type'] == 'FeatureCollection'
    assert result['features'][0]['properties']['style']['opacity'] == 0.7