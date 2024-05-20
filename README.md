# Geochron
[![Unit Tests](https://github.com/etalbert102/geochron/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/etalbert102/geochron/actions/workflows/unit-tests.yml)

A companion package to geostructures (https://github.com/ccbest/geostructures) enabling geo-spatial-temporal data structures



### Installation

Geochron is available on PYPI
```
$ pip install geochron 
```

#### Optional Dependencies
Geotime does not require any of the below dependencies to function, however some functionality uses:
* plotly (visualization)
* networkx (chron-nets)
* timehash (geotimehash)

### Overview

Geotime enables various ways of displaying and structuring geo-spatial-temporal data

The methods currently supported are:
* time hexes H3 Geohashes with second dimension time (Original Niemeyer can also be used)
* chron-nets (https://www.nature.com/articles/s41467-020-17634-2)
* geotimehash (https://isprs-annals.copernicus.org/articles/IV-4-W2/31/2017/isprs-annals-IV-4-W2-31-2017.pdf)


#### Basic Functionality
The primary and simplest use case is converting a geostructures FeatureCollection to another datastructure.
Geostructures FeatureCollections can take most major geospatial standards like shapefiles and geopandas. See geostructures documentation. 
```python
from geochron import convert

timehex_output = convert(fcol=Feature_Collection_of_time_shapes, datastructure= "timehex",
hour_interval= 1, res= 10)

chronnet_output = convert(fcol=Feature_Collection_of_time_shapes, datastructure= "chronnet",
hour_interval= 1, res= 10, self_loop = True, mode = "directed")

geotimehash_output = convert(fcol=Feature_Collection_of_time_shapes, datastructure= "geotimehash",
hour_interval= 1, res= 10, precision = 8)

```


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

