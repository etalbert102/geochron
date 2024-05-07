import sys

from geochron._version import __version__  # noqa: F401
from geochron.utils.conditional_imports import ConditionalPackageInterceptor
from geochron.convert import convert

ConditionalPackageInterceptor.permit_packages(
    {
        'networkx': 'networkx>=3.0,<4.0',
        'plotly': 'plotly>=5,<6',
    }
)
sys.meta_path.append(ConditionalPackageInterceptor)  # type: ignore

__all__ = [
    'convert'

]