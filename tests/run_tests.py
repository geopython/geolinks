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

import json
import os.path
import unittest

from geolinks import sniff_link


class GeolinksTest(unittest.TestCase):
    """Test suite for package Foo"""
    def setUp(self):
        """setup test fixtures, etc."""

        test_data = None

        if os.path.exists('test_data.json'):
            test_data = 'test_data.json'
        elif os.path.exists('tests/test_data.json'):
            test_data = 'tests/test_data.json'
        else:
            raise FileNotFoundError()

        with open(test_data) as f:
            self.test_data = json.load(f)

    def tearDown(self):
        """return to pristine state"""
        pass

    def test_link_types(self):
        """simple link type tests"""

        for test in self.test_data['test_data']:
            self.assertEqual(sniff_link(test['link'], probe=test.get('probe',False), first=test.get('first',True)), test['expected'],
                             'Expected %s and %s to be equal' %
                             (test['link'], test['expected']))


if __name__ == '__main__':
    unittest.main()
