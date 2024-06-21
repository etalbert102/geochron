"""Folium helpers"""
import json
from typing import Any, Callable, Optional, Union
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
    elif isinstance(cmap, list):
        used_cmap = LinearColormap(colors= cmap, \
        vmin=min_color, vmax=max_color)
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

def normalize(value: float, min_val: float, max_val: float):
    """
    Normalize a value on a scale from 1 to 0 based on a given
    min and max value.

    Args:
        value: a value
        min_val: the minimum value
        max_val: the maximum value 

    Returns:
        a scaled value between 1 to 0
    """
    if max_val == min_val:
        raise ValueError("max_val and min_val cannot be equal (division by zero)")
    scaled_value = (value - min_val) / (max_val - min_val)
    return scaled_value

def constant_return(value: float, constant: Any):
    """
    Returns a constant when fed a value  
    Args:
        value: any value
        constant: any constant
    Returns:
        the specified constant 
    """
    return constant

def add_hashmap_properties(original_hashmap:dict, time:pd.Timestamp, opacity: Union[float, str] \
                            , cmap: Union[Optional[Callable], list] = None):
    """
    Adds properties to the hashmap necessary for display.

    Args:
        original_hashmap: a hashmap
        time: time of hashmap
        cmap: a Branca colormap or a list of colors 
        opacity: desired opacity of shapes takes key word gradient
        to vary opacity based on weight of shape in the time period
    Returns:
        a GeoJson FeatureCollection
    """
    new_dict = {}
    removed_empty = {key: value for key, value in original_hashmap.items() if value != 0}

    if len(removed_empty) == 0:
        color_min = 0
        color_max = 0
    else:
        max_key = max(removed_empty, key=removed_empty.get) # type: ignore[arg-type]
        min_key = min(removed_empty, key=removed_empty.get) # type: ignore[arg-type]
        color_min = removed_empty[min_key]
        color_max = removed_empty[max_key]

    if cmap is None:
        used_cmap = LinearColormap(colors=['blue','red'], \
        vmin= color_min, vmax= color_max)
    elif isinstance(cmap, list):
        used_cmap = LinearColormap(colors= cmap, \
        vmin= color_min, vmax= color_max)
    else:
        used_cmap = cmap

    if opacity == "gradient":
        used_opacity = lambda x: normalize(x,min_val = color_min, max_val= color_max)
    else:
        used_opacity = lambda x: constant_return(x, constant= opacity)

    for key, value in removed_empty.items():
        new_dict[key] = {'popup': 'weight= ' + str(value) +
                    '<br> center(lat,lon)= ' + str(h3.h3_to_geo(key)), 
                    'time': time,'style':{'opacity': used_opacity(value), 'color': used_cmap(value),
                                               'fillOpacity': used_opacity(value)}}
    return new_dict

def timehex_timestampedgeojson(timehex: pd.DataFrame, opacity: Union[float, str] = .7 \
                               , cmap: Union[Optional[Callable], list] = None):
    """
    Formats a timehex into the correct data format for Folium's timestampedgeojson

    Args:
        timehex: A timehex dataframe
        opacity: desired opacity of shapes takes key word gradient
        to vary opacity based on weight of shape in the time period
        cmap: a Branca colormap or a list of colors 
    Returns:
        a GeoJson FeatureCollection
    """
    start_time_list = timehex['start_time'].tolist()
    select_timehex = timehex.drop(['interval', 'start_time', 'end_time'], axis=1).fillna(0)
    list_hashmaps = select_timehex.to_dict('records')
    polygon_list:list = []

    for hashmap, start_time in zip(list_hashmaps, start_time_list):
        hashmap_properties= add_hashmap_properties(original_hashmap = hashmap,\
        time = start_time, opacity = opacity, cmap= cmap)
        polygons = {h3_to_geopolygon(k, properties= v) for k,v in hashmap_properties.items()}
        polygon_list.extend(polygons)

    return FeatureCollection(polygon_list).to_geojson()
