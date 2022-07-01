# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2022 Tom Kralidis
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
import sys

import click
from owslib.wms import WebMapService as WMS
from owslib.wfs import WebFeatureService as WFS
from owslib.ogcapi.features import Features as OAPIF
from owslib.ogcapi.coverages import Coverages as OAPIC
from owslib.ogcapi.records import Records as OAPIR
from owslib.wcs import WebCoverageService as WCS
from owslib.csw import CatalogueServiceWeb as CSW
from owslib.wps import WebProcessingService as WPS
from owslib.sos import SensorObservationService as SOS
from owslib.wmts import WebMapTileService as WMTS

LOGGER = logging.getLogger(__name__)

__version__ = '0.2.dev0'


def CLICK_OPTION_VERBOSITY(f):
    logging_options = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

    def callback(ctx, param, value):
        if value is not None:
            logging.basicConfig(stream=sys.stdout,
                                level=getattr(logging, value))
        return True

    return click.option('--verbosity', '-v',
                        type=click.Choice(logging_options),
                        help='Verbosity',
                        callback=callback)(f)

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


def sniff_link(url, extended=False, first=True):
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
        if (extended):
            protocol = []
            #for each servicetype, head out to see if it is valid
            try: 
                wms = WMS(link)
                if (wms.identification.type == 'OGC:WMS'):
                    if (first):
                        return wms.identification.type
                    else:
                        protocol.append(wms.identification.type)
            except:
                pass # No need to log?
            try: 
                wmts = WMTS(link)        
                if (wmts.identification.type == 'OGC:WMTS'):
                    if (first):
                        return wmts.identification.type
                    else:
                        protocol.append(wmts.identification.type)
            except:
                pass
            try:
                wps = WPS(link, verbose=False, skip_caps=True)
                wps.getcapabilities()
                if (wps.identification.type == 'OGC:WPS'):
                    if (first):
                        return wps.identification.type
                    else:
                        protocol.append(wps.identification.type)
            except:
                pass 
            try:
                wfs = WFS(link)
                if (wfs.identification.type == 'OGC:WFS'):
                    if (first):
                        return wfs.identification.type
                    else:
                        protocol.append(wfs.identification.type)
            except:
                pass
            try:
                csw = CSW('http://geodiscover.cgdi.ca/wes/serviceManagerCSW/csw')
                if (csw.identification.type == 'OGC:CSW'):
                    if (first):
                        return csw.identification.type
                    else:
                        protocol.append(csw.identification.type)
            except:
                pass
            try:
                wcs = WCS(link)
                if (wcs.identification.type == 'OGC:WCS'):
                    if (first):
                        return wcs.identification.type
                    else:
                        protocol.append(wcs.identification.type)
            except:
                pass
            try:
                sos = SOS(link)
                if (sos.identification.type == 'OGC:SOS'):
                    if (first):
                        return sos.identification.type
                    else:
                        protocol.append(sos.identification.type)
            except:
                pass
            try: 
                oapir = OAPIR(link)
                if (oapir.conformance()):
                    if (first):
                        return "OGCAPI:records"
                    else:
                        protocol.append("OGCAPI:records")
            except:
                pass
            try: 
                oapif = OAPIF(link)
                if (oapir.conformance()):
                    if (first):
                        return "OGCAPI:features"
                    else:
                        protocol.append("OGCAPI:features")
            except:
                pass
            try: 
                oapic = OAPIC(link)
                if (oapir.conformance()):
                    if (first):
                        return "OGCAPI:coverages"
                    else:
                        protocol.append("OGCAPI:coverages")
            except:
                pass

            if len(protocol) == 1:
                protocol = protocol[0]

        else:
            LOGGER.info('No link type detected')

    return protocol


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@click.group()
def link():
    """Link utilities"""
    pass


@click.command()
@click.argument('link')
@CLICK_OPTION_VERBOSITY
def sniff(link, verbosity):
    """Sniff link"""

    click.echo(f'Sniffing link: {link}')

    link_type = sniff_link(link)

	if isinstance(link_type, str):
	    click.echo(f'Link type: {link_type}')
	else:
		click.echo(f'Link types: {link_type.join(",")}')

link.add_command(sniff)
cli.add_command(link)
