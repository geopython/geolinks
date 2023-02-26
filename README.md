[![Build Status](https://github.com/geopython/geolinks/workflows/build%20%E2%9A%99%EF%B8%8F/badge.svg)](https://github.com/geopython/geolinks/actions)

# geolinks

Utilities to deal with geospatial links.  Working implementation
of the Cat-Interop work at https://github.com/OSGeo/Cat-Interop

## Installation

geolinks is best installed and used within a Python virtualenv.

### Requirements

* Python 3 and above
* Python [virtualenv](https://virtualenv.pypa.io/) package

### Dependencies

Dependencies are listed in [requirements.txt](requirements.txt). Dependencies
are automatically installed during geolinks's installation.

### Installing the Package

from source:
```bash
python3 -m venv my-env
cd my-env
. bin/activate
git clone https://github.com/geopython/geolinks.git
cd geolinks
python setup.py build
python setup.py install
```

via pip:
```bash
pip install geolinks
```

## Running

```bash
geolinks link sniff 'http://host/wms?service=WMS'
```

## Using the API from Python

```python
>>> from geolinks import sniff_link
>>> sniff_link('http://host/wms?service=WMS')
'OGC:WMS'
>>> sniff_link('http://host/wms?service=WPS')
'OGC:WPS'
>>> sniff_link('http://host/wms?service=CSW')
'OGC:CSW'
>>> sniff_link('http://host/data/roads.kmz')
'OGC:KML'
>>> sniff_link('http://host/data/roads.kml')
'OGC:KML'
```

### Running Tests

```bash
# via setuptools
python setup.py test
# manually
cd tests
python run_tests.py
```

## Development

### Setting up a Development Environment

Same as installing a package.  Use a virtualenv.  Also install developer
requirements:

```bash
pip install -r requirements-dev.txt
```

## Releasing

```bash
vi geolinks/__init__.py
git commit -m 'update release version' geolinks/__init__.py
vi debian/changelog  # add changelog entry and summary of updates
# push changes
git push origin master
git tag -a x.y.z -m 'tagging release x.y.z'
# push tag
git push --tags
rm -fr build dist *.egg-info
python setup.py sdist bdist_wheel --universal
twine upload dist/*
```

### Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

### Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/geopython/geolinks/issues).

## Contact

* [Tom Kralidis](https://github.com/tomkralidis)
