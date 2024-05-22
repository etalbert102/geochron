import sys

from geotime._version import __version__  # noqa: F401
from geotime.utils.conditional_imports import ConditionalPackageInterceptor

ConditionalPackageInterceptor.permit_packages(
    {
        'plotly': 'plotly>=5,<6',
    }
)
sys.meta_path.append(ConditionalPackageInterceptor)  # type: ignore

