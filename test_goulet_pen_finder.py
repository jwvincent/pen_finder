#!/usr/env/bin python3

import unittest
from unittest import mock
from goulet_pen_finder import PenFinderMethods
import urllib.request
import ssl
from bs4 import BeautifulSoup
import json
import csv
import time

class TestPenFinderMethods(unittest.TestCase):

    def setUp(self):
        with open('test_goulet_pen_page.html') as pen_page:
            self.pen_soup = BeautifulSoup(pen_page, html_parser)

    global html_parser
    html_parser = 'html.parser'


    """This needs to be a string"""
    global base_page
    with open('test_goulet_base_page.html') as f:
        base_page = f.read()

    global expected_technical_specs
    expected_technical_specs = {"Condition":"Feathery", "Brand":"FLETCHER", "Type":"Quill", "Body Material":"Keratin", "Cap Rotations":"300", "Cap Type":"Literal", "Grip Material":"Mithril", "Diameter - Grip":"113.0mm (560.5in)", "Length - Body":"1243.9mm (40.9in)", "Length - Cap":"444.0mm (11.8in)"}

    global expected_name
    expected_name = 'Turkey Quill'

    global expected_price
    expected_price = 179.00

    global expected_diameter
    expected_diameter = 113.0

    global c
    c = PenFinderMethods()


    @mock.patch('urllib.request.urlopen')

    def test_find_all_pens(self, mock_page_request):
        mock_page_request.return_value = base_page
        test_data = ["https://www.gouletpens.com/collections/all-fountain-pens/products/Captian_Marval", "https://www.gouletpens.com/collections/all-fountain-pens/products/Deadpool", "https://www.gouletpens.com/collections/all-fountain-pens/products/Thor", "https://www.gouletpens.com/collections/all-fountain-pens/products/The_Black_Panther", "https://www.gouletpens.com/collections/all-fountain-pens/products/The_Silver_Surfer", "https://www.gouletpens.com/collections/all-fountain-pens/products/Captian_America", "https://www.gouletpens.com/collections/all-fountain-pens/products/Iron_Man", "https://www.gouletpens.com/collections/all-fountain-pens/products/Dr_Strange", "https://www.gouletpens.com/collections/all-fountain-pens/products/Batman", "https://www.gouletpens.com/collections/all-fountain-pens/products/Wonder_Woman", "https://www.gouletpens.com/collections/all-fountain-pens/products/Aquaman", "https://www.gouletpens.com/collections/all-fountain-pens/products/The_Flash"]

        self.assertSetEqual(set(c.find_all_pens(1,52)),set(test_data))
        self.assertEqual(mock_page_request.call_count, 52)


    def test_get_pen_name(self):
        self.assertEqual(c.get_pen_name(self.pen_soup), expected_name)

    def test_get_pen_price(self):
        self.assertEqual(c.get_pen_price(self.pen_soup), expected_price)

    def test_get_technical_specs(self):
        self.assertDictEqual(c.get_technical_specs(self.pen_soup), expected_technical_specs)

    @mock.patch('goulet_pen_finder.PenFinderMethods.get_technical_specs', return_value=expected_technical_specs)
    def test_get_pen_grip_diameter(self, mock_technical_specs):
        self.assertEqual(PenFinderMethods.get_pen_grip_diameter(PenFinderMethods, self.pen_soup), expected_diameter)

    @mock.patch('goulet_pen_finder.PenFinderMethods.get_pen_grip_diameter', return_value=expected_diameter)
    @mock.patch('goulet_pen_finder.PenFinderMethods.get_technical_specs', return_value=expected_technical_specs)
    @mock.patch('goulet_pen_finder.PenFinderMethods.get_pen_name', return_value=expected_name)
    @mock.patch('goulet_pen_finder.PenFinderMethods.get_pen_price', return_value=expected_price)
    def test_format_row(self,mock_price, mock_pen_name, mock_technical_specs,  mock_grip_diameter):
        test_url = 'www.place_holder.com'
        expected_row = [expected_name, expected_price, 'Keratin', 'Literal', 'Mithril', expected_diameter, test_url]
        self.assertListEqual(PenFinderMethods.format_row(PenFinderMethods, self.pen_soup, test_url), expected_row)

if __name__ == '__main__':
    unittest.main()
