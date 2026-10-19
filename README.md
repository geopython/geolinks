[![Build Status](https://github.com/geopython/geolinks/workflows/build%20%E2%9A%99%EF%B8%8F/badge.svg)](https://github.com/geopython/geolinks/actions)

# geolinks

Utilities to deal with geospatial links.  Working implementation
of the Cat-Interop work at https://github.com/OSGeo/Cat-Interop

## Installation

### pip

Install latest stable version from [PyPI](https://pypi.org/project/geolinks)

```bash
pip3 install geolinks
```

### From source

```bash
python3 -m venv geolinks
cd geolinks
. bin/activate
git clone https://github.com/geopython/geolinks.git
cd geolinks
pip3 install .
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
python3 tests/run_tests.py
```

## Development

```bash
python3 -m venv geolinks
cd geolinks
source bin/activate
git clone https://github.com/geopython/geolinks.git
cd geolinks
pip3 install .
pip3 install ".[dev]"
```

## Releasing

```bash
# create release (x.y.z is the release version)
vi pyproject.toml  # update [project]/version
git commit -am 'update release version x.y.z'
git push origin master
git tag -a x.y.z -m 'tagging release version x.y.z'
git push --tags

# upload to PyPI
rm -fr build dist *.egg-info
python3 -m build
twine upload dist/*

# publish release on GitHub (https://github.com/geopython/geolinks/releases/new)

# bump version back to dev
vi pyproject.toml  # update [project]/version
git commit -am 'back to dev'
git push origin master
```

### Code Conventions

* [PEP8](https://www.python.org/dev/peps/pep-0008)

### Bugs and Issues

All bugs, enhancements and issues are managed on [GitHub](https://github.com/geopython/geolinks/issues).

## Contact

* [Tom Kralidis](https://github.com/tomkralidis)
