"""Folium helpers"""
import json
import pandas as pd
from branca.colormap import LinearColormap 
from typing import Callable, Optional

def timehex_styledict(timehex: pd.DataFrame, opacity= float(.7), cmap:Optional[Callable] = None):
    """
    Creates a styledict appropriate for a folium TimeSliderChoropleth from
    a timehex dataframe

    Args:
        timehex: A timehex pandas dataframe 

    Returns:
        A style dictionary suitable to use with folium's 
        TimeSliderChoropleth
    """
    timehex_duplicate = timehex.copy()
    timehex_duplicate['time'] = timehex_duplicate['start_time'].astype("int64") // 10 ** 9

    select_timehex = timehex_duplicate.drop(['interval', 'start_time', 'end_time'], axis=1)

    timehex_long = select_timehex.melt(id_vars='time', var_name='id', value_name='value')
    
    timehex_long = timehex_long.fillna(0)

    #color scale 
    max_color = max(timehex_long['value'])
    min_color = min(timehex_long['value'])
    if cmap == None:
        used_cmap = LinearColormap(colors=['blue','red'], vmin=min_color, vmax=max_color)
    else:
        used_cmap = cmap

    styledict = {
    str(id): {
        time: {'color': used_cmap(color), 'opacity': 0 if color == 0 else opacity} 
        for time, color in zip(timehex_long[timehex_long['id'] == id]['time'], timehex_long[timehex_long['id'] == id]['value'])
    } 
    for id in timehex_long['id'].unique()
    }

    return styledict

def h3_to_geojson(h3_hashmap):
    import h3
    # Initialize an empty list to store the features
    features = []

    # Iterate over the H3 hashmap
    for h3_index, properties in h3_hashmap.items():
        # Convert the H3 index to a GeoJSON polygon
        geojson_polygon = h3.h3_to_geo_boundary(h3_index, geo_json=True)

        # Create a GeoJSON feature for the H3 index
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [geojson_polygon]
            },
            "properties": properties,
            "id" : h3_index
        }

        # Add the feature to the list of features
        features.append(feature)

    # Create a GeoJSON FeatureCollection
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }

    # Return the FeatureCollection as a JSON string
    return json.dumps(feature_collection)

def timehex_backgroundata(timehex: pd.DataFrame):
    select_timehex = timehex.drop(['interval', 'start_time', 'end_time'], axis=1)
    hashmap = select_timehex.to_dict()
    backgroundata = h3_to_geojson(hashmap)

    return backgroundata