"""Package build script"""
import os
import re
import setuptools

ver_file = f'geochron{os.sep}_version.py'
__version__ = None

# Pull package version number from _version.py
with open(ver_file, 'r') as f:
    for line in f.readlines():
        if re.match(r'^\s*#', line):  # comment
            continue

        ver_line = line
        verstr = re.match(r"^.*=\s+'(v\d+\.\d+\.\d+(?:\.[a-zA-Z0-9]+)?)'", ver_line)
        if verstr is not None and len(verstr.groups()) == 1:
            __version__ = verstr.groups()[0]
            break

    if __version__ is None:
        raise EnvironmentError(f'Could not find valid version number in {ver_file}; aborting setup')

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geochron",
    version=__version__,
    author="Eli Talbert",
    author_email="",
    description="A companion package to geostructures enabling geo-spatial-temporal data structures.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/etalbert102/geochron",
    packages=setuptools.find_packages(
        include=('geochron*', ),
        exclude=('*tests', 'tests*')
    ),
    package_data={"geochron": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    install_requires=[
        'geostructures>= 0.10.0, <1.0',
        'numpy>=1,<2',  
        'pandas>=2,<3'
    ],
)
