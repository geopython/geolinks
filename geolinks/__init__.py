# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2023 Tom Kralidis
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
from typing import Union

import click

LOGGER = logging.getLogger(__name__)

__version__ = '0.2.3'


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


def inurl(needles, haystack, position='any') -> bool:
    """
    convenience function to find a given value in a URL

    :param needles: `list` of patterns to test
    :param haystack: value to search / detect for patterns

    returns: `bool` of assessment
    """

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


def sniff_link(url) -> Union[str, None]:
    """
    performs basic heuristics to detect what the URL is

    :param url: `str` of URL

    :returns: possible link type or `None`
    """

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

    click.echo(f'Link type: {link_type}')


link.add_command(sniff)
cli.add_command(link)
