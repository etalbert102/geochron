# Contributor Guide

First and foremost, thank you for your interest in helping!

We welcome contributions in the form of merge requests based on the `main` branch, and in the form of issues describing
any problems you experience with this code. Following these guidelines will reduce friction and improve the speed with 
which your merge request or issue will be reviewed and resolved.

### For New Contributors

We welcome your participation in all aspects of this project!

While this project is in a pre-1.0 state it will use the 
[`github-flow`](https://docs.github.com/en/get-started/quickstart/github-flow) workflow. 

### Development / Style Guidelines

Correctness is necessary; efficiency is desirable. Pull requests will be scrutinized for both, but we will 
happily work with you on performance improvements.

Pull requests must be limited to a singular logical enhancement (e.g. a single bug fix, feature, or documentation 
update). Pull requests encompassing multiple enhancements will be reviewed on a case-by-case basis but most likely 
rejected, and we will ask you to cherry-pick your changes into multiple pull requests.

Type assertions are required in virtually all instances except where extremely impractical (will be reviewed on a case-
by-case basis). All pull requests must pass type checking via mypy.

Over-document when in doubt and when meaningful.

### Optional dependencies
Geochron maintains a formal definition of "optional" dependencies (third-party packages
required for additional functionality but not required for core operation). These dependencies will still be 
scrutinized for necessity, however are much more likely to be accepted provided that their introduction does not 
interfere with core functionality.

Whenever an optional dependency is utilized it must be imported only within the scope of its usage so that code
which does not rely on the dependency may still be compiled.

### Definition Order
Unless otherwise required, definitions in modules should follow the below order
1. Constants
2. Functions
3. Classes

Furthermore, class method/property definitions should be structured according to:
1. Class variables
2. Magic methods (\_\_init__() should always be first regardless of alphabetic order)
3. Properties
4. Private methods
5. Public methods

In all instances of the above, definitions should be sub-ordered alphabetically (init being the only exception).

Tests should follow the same order as defined in the actual code.

### Pull Request Requirements

Code submitted within a merge request should be well-structured and commented. Specifically, all code must:
* Pass linting checks over 9.0 (pylint)
* Pass type assertions (mypy)
* Pass all unit tests (pytest)
* Maintain 100% unit test coverage, except in extremely rare circumstances

### PEP8 Divergences

Geostructures follows Python's PEP8 style guidance, with the following exceptions:

* Tabs are preferred over spaces.