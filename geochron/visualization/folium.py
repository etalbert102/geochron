"""Folium helpers"""
import json
from typing import Callable, Optional
import h3
import pandas as pd
from branca.colormap import LinearColormap
from geostructures.geohash import h3_to_geopolygon
from geostructures import FeatureCollection

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
    if cmap is None:
        used_cmap = LinearColormap(colors=['blue','red'], vmin=min_color, vmax=max_color)
    else:
        used_cmap = cmap


    # Vectorized operations for creating styledict
    styledict = timehex_long.groupby('id').apply(lambda df: df.set_index('time')['value']\
    .apply(lambda x: {'color': used_cmap(x), 'opacity': 0 if x == 0 else opacity})\
    .to_dict()).to_dict()

    return styledict



def h3_to_geojson(h3_hashmap):
    """
    Converts a H3 hashmap to a GeoJSON FeatureCollection

    Args:
        h3_hashmap: A H3 hashmap

    Returns:
        A GeoJSON FeatureCollection as a JSON string 
    """
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
    """
    Formats backgroundata polygons appropriate for a folium TimeSliderChoropleth from
    a timehex dataframe

    Args:
        timehex: A timehex dataframe

    Returns:
        a GeoJson FeatureCollection
    """
    select_timehex = timehex.drop(['interval', 'start_time', 'end_time'], axis=1)
    hashmap = select_timehex.to_dict()
    backgroundata = h3_to_geojson(hashmap)

    return backgroundata

def add_hashmap_properties(original_hashmap:dict, time, cmap: Callable, opacity= float(.7)):
    """
    Formats backgroundata polygons appropriate for a folium TimeSliderChoropleth from
    a timehex dataframe

    Args:
        timehex: A timehex dataframe

    Returns:
        a GeoJson FeatureCollection
    """
    new_dict = {}
    removed_empty = {key: value for key, value in original_hashmap.items() if value != 0}
    for key, value in removed_empty.items():
        new_dict[key] = {'popup': 'weight= ' + str(value) +
                         '<br> center(lat,lon)= ' + str(h3.h3_to_geo(key)), 
                         'time': time,'style':{'opacity': opacity, 'color': cmap(value)}}
    return new_dict

def timehex_timestampedgeojson(timehex: pd.DataFrame, cmap:Optional[Callable] = None):
    """
    Formats a timehex into the correct data format for Folium's timestampedgeojson

    Args:
        timehex: A timehex dataframe

    Returns:
        a GeoJson FeatureCollection
    """
    start_time_list = timehex['start_time'].tolist()
    select_timehex = timehex.drop(['interval', 'start_time', 'end_time'], axis=1).fillna(0)
    list_hashmaps = select_timehex.to_dict('records')
    polygon_list:list = []

    #color scale
    max_color = select_timehex.values.max()
    min_color = select_timehex.values.min()
    if cmap is None:
        used_cmap = LinearColormap(colors=['blue','red'], vmin=min_color, vmax=max_color)
    else:
        used_cmap = cmap

    for hashmap, start_time in zip(list_hashmaps, start_time_list):
        hashmap_properties= add_hashmap_properties(hashmap, start_time, used_cmap)
        polygons = {h3_to_geopolygon(k, properties= v) for k,v in hashmap_properties.items()}
        polygon_list.extend(polygons)

    return FeatureCollection(polygon_list).to_geojson()
