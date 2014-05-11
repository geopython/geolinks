geolinks
========

Utilities to deal with geospatial links

Install
-------

```bash
pip install geolinks

```

Use
---

```python
>>> from geolinks.link_types import sniff_link
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
