# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2014 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import logging

LOGGER = logging.getLogger(__name__)

__version__ = '0.2.0'


def inurl(needles, haystack, position='any'):
    """convenience function to make string.find return bool"""

    count = 0

    # lowercase everything to do case-insensitive search
    haystack2 = haystack.lower()

    for needle in needles:
        needle2 = needle.lower()
        if position == 'any':
            if haystack2.find(needle2) > -1:
                count += 1
        elif position == 'end':
            if haystack2.endswith(needle2):
                count += 1
        elif position == 'begin':
            if haystack2.startswith(needle2):
                count += 1

    # assessment
    if count > 0:
        return True
    return False


def sniff_link(url):
    """performs basic heuristics to detect what the URL is"""

    protocol = None
    link = url.strip()

    # heuristics begin
    if inurl(['service=CSW', 'request=GetRecords'], link):
        protocol = 'OGC:CSW'
    elif inurl(['service=SOS', 'request=GetObservation'], link):
        protocol = 'OGC:SOS'
    elif inurl(['service=WCS', 'request=GetCoverage'], link):
        protocol = 'OGC:WCS'
    elif inurl(['service=WFS', 'request=GetFeature'], link):
        protocol = 'OGC:WFS'
    elif inurl(['service=WMS', 'request=GetMap'], link):
        protocol = 'OGC:WMS'
    elif inurl(['service=WPS', 'request=Execute'], link):
        protocol = 'OGC:WPS'
    elif inurl(['arcims'], link):
        protocol = 'ESRI:ArcIMS'
    elif inurl(['arcgis'], link):
        protocol = 'ESRI:ArcGIS'
    elif inurl(['mpk'], link, 'end'):
        protocol = 'ESRI:MPK'
    elif inurl(['opendap'], link):
        protocol = 'OPeNDAP:OPeNDAP'
    elif inurl(['ncss'], link):
        protocol = 'UNIDATA:NCSS'
    elif inurl(['cdmremote'], link):
        protocol = 'UNIDATA:CDM'
    elif inurl(['gml'], link, 'end'):
        protocol = 'OGC:GML'
    elif inurl(['htm', 'html', 'shtml'], link, 'end'):
        protocol = 'WWW:LINK'
    # extra tests
    elif all([inurl(['census.gov/geo/tiger'], link),
              inurl(['zip'], link, 'end')]):
        protocol = 'ESRI:SHAPEFILE'
    elif inurl(['7z', 'bz2', 'gz', 'rar', 'tar.gz', 'tgz', 'zip'],
               link, 'end'):
        protocol = 'WWW:DOWNLOAD'
    elif inurl(['kml', 'kmz'], link, 'end'):
        protocol = 'OGC:KML'
    else:
        LOGGER.info('No link type detected')

    return protocol
