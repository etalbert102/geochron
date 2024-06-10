<picture align="center">
  <source media="(prefers-color-scheme: dark)" srcset="./static/dark_logo.png">
  <img alt="Geochron Logo" src="./static/white_logo.png">
</picture>

# Geochron
[![Unit Tests](https://github.com/etalbert102/geochron/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/etalbert102/geochron/actions/workflows/unit-tests.yml)

A companion package to geostructures (https://github.com/ccbest/geostructures) enabling geo-spatial-temporal data structures



### Installation

Geochron is available on PYPI
```
$ pip install geochron 
```

#### Optional Dependencies
Geochron does not require any of the below dependencies to function, however some functionality uses:
* networkx (chron-nets/geosynchnet)
* timehash (geotimehash)

### Overview

Geochron enables various ways of displaying and structuring geospatial-temporal data

The methods currently supported are:
* time hexes H3 Geohashes with second dimension time (Original Niemeyer can also be used)
* chron-net (https://www.nature.com/articles/s41467-020-17634-2)
* geotimehash (https://isprs-annals.copernicus.org/articles/IV-4-W2/31/2017/isprs-annals-IV-4-W2-31-2017.pdf)
* geosynchnet (geographic synchronous networks)


#### Basic Functionality
The primary and simplest use case is converting a geostructures FeatureCollection to another datastructure.
Geostructures FeatureCollections can take most major geospatial standards like shapefiles and geopandas. See geostructures documentation. 
```python
import datetime as dt
from geochron import convert_timehex, convert_chronnet, convert_geotimehash
from geostructures.geohash import H3Hasher

hasher = H3Hasher(resolution=11)

timehex_output = convert_timehex(fcol=Feature_Collection_of_time_shapes,
time_delta= dt.timedelta(hours=1), hash_func= hasher.hash_collection)

chronnet_output = convert_chronnet(fcol=Feature_Collection_of_time_shapes,
time_delta= dt.timedelta(hours=1), hash_func= hasher.hash_collection, self_loops = True, mode = "directed")

geotimehash_output = convert_geotimehash(fcol=Feature_Collection_of_time_shapes, precision = 8,
hash_func= hasher.hash_collection)

geosynchnet_output = convert_geosynchnet(fcol=Feature_Collection_of_time_shapes, 
time_delta= dt.timedelta(hours=1), hash_func= hasher.hash_collection)

```
Geochron also provides helper functions for visualization using popular libraries like Folium and Pydeck. These helpers 
arlocated in geochron.visualizations

## More Information

For an more in-depth introduction, please review our collection of [Jupyter notebooks](./notebooks).



### Reporting Issues / Requesting Features

The Geochron team uses Github issues to track development goals. Please include as much detail as possible so we can effectively triage your request.

### Contributing

We welcome all contributors! Please review [CONTRIBUTING.md](./CONTRIBUTING.md) for more information.

### Developers
Eli Talbert (Sr. Data Scientist/PhD/Project Owner)\
https://github.com/etalbert102 

Carl Best (Sr. Data Scientist)\
https://github.com/ccbest/

