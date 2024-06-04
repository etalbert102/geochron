import json
import pandas as pd
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

    # Check that the result is a dictionary
    assert isinstance(result, dict)

    # Check that the dictionary has the expected keys and values
    for key in ['hex1', 'hex2', 'hex3']:
        assert key in result
        assert isinstance(result[key], dict)
        for time_key in result[key]:
            assert 'color' in result[key][time_key]
            assert 'opacity' in result[key][time_key]


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
