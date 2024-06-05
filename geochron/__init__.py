"""Init"""
import sys

from geochron._version import __version__  # noqa: F401
from geochron.utils.conditional_imports import ConditionalPackageInterceptor
from geochron.chronnet import convert_chronnet
from geochron.timehex import convert_timehex
from geochron.geotimehash import convert_geotimehash
from geochron.geosynchnet import convert_geosynchnet

ConditionalPackageInterceptor.permit_packages(
    {
        'networkx': 'networkx>=3.0,<4.0',
        'timehash': 'timehash>=1.2,<2',
        'branca': 'branca>=0.7.2,<1.0',
    }
)
sys.meta_path.append(ConditionalPackageInterceptor)  # type: ignore

__all__ = [
    'convert_chronnet',
    'convert_timehex',
    'convert_geotimehash',
    'convert_geosynchnet' 
]
