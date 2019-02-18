import unittest
import os
import sys
import re
from dbeurive.ispdb.isp import Isp
from pprint import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

class TestIsp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        xmlreg = re.compile('.xml$')
        self.xml_files = [f for f in os.listdir(self.data_path) if os.path.isfile(os.path.join(self.data_path, f)) and xmlreg.search(f) is not None]

    def setUp(self):
        pass

    # Test that all XML files can be loaded.
    def test_init1(self):
        for xml_file in self.xml_files:
            xml_path = os.path.join(self.data_path, xml_file)
            with open(xml_path, 'r') as fd:
                # noinspection PyUnusedLocal
                isp = Isp(fd.read())

    def test_smtp_counts(self):

        # SMTP: 0
        isp_name = 'cloudnine-net.jp.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(0, isp.get_smtp_configs_count())

        # SMTP: 1
        isp_name = '126.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(1, isp.get_smtp_configs_count())

        # SMTP: 2
        isp_name = 'moscowmail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(2, isp.get_smtp_configs_count())

        # SMTP: 3
        isp_name = 'thinline.cz.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(3, isp.get_smtp_configs_count())

    def test_pop3_counts(self):

        # POP3: 0
        isp_name = '126.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(0, isp.get_pop3_configs_count())

        # POP3: 1
        isp_name = 'lazy.dk.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(1, isp.get_pop3_configs_count())

        # POP3: 2
        isp_name = 'uymail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(2, isp.get_pop3_configs_count())

    def test_imap_counts(self):

        # IMAP: 0
        isp_name = 'ybb.ne.jp.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(0, isp.get_imap_configs_count())

        # IMAP: 1
        isp_name = 'lazy.dk.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(1, isp.get_imap_configs_count())

        # IMAP: 2
        isp_name = 'uymail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertEqual(2, isp.get_imap_configs_count())

    def test_invalid(self):
        isp_name = 'cloudnine-net.jp.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertFalse(isp.is_valid())

    def test_valid(self):
        isp_name = 'uymail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
            self.assertTrue(isp.is_valid())
