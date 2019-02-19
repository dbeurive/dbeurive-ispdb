import unittest
import os
import sys
import re
from dbeurive.ispdb.web.parser import Parser
from pprint import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

class TestParser(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
        self.html_path = os.path.join(self.data_path, 'ispdb.html')

    def setUp(self):
        pass

    def test_parser(self):

        # noinspection PyUnusedLocal
        html: str = None
        with open(self.html_path, 'r') as fd:
            html = fd.read()

        regex = re.compile('<img src="/icons/text\.gif" alt="\[TXT\]"></td><td><a href="([^"]+)">')
        list_of_isps = regex.findall(html)
        parser = Parser()
        parser.feed(html)
        ips = parser.get_isps()
        self.assertEqual(len(list_of_isps), len(ips))
        self.assertEqual(list_of_isps, list(map(lambda x: x.name, ips)))

        regex = re.compile('<td align="right">(\d+(\.\d+)?K?)\s?</td>')
        list_of_sizes = regex.findall(html)
        list_of_sizes = list(map(lambda x: x[0], list_of_sizes))
        self.assertEqual(len(list_of_sizes), len(ips))
        self.assertEqual(list_of_sizes, list(map(lambda x: x.size, ips)))
