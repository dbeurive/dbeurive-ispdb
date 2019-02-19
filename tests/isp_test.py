# To get data about the pull of XML files, you can run the tools listed below:
#
# - tests/bin/analyze.py
# - tests/bin/get_xml.py

import unittest
import os
import sys
import re
from dbeurive.ispdb.isp import Isp

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

    def test_smtp_content(self):

        # --------------------------------------------------------------------

        isp_name = 'thinline.cz.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_smtp_configs()

        #     <outgoingServer type="smtp">
        #       <hostname>smtp.cesky-hosting.cz</hostname>
        #       <port>465</port>
        #       <socketType>SSL</socketType>
        #       <authentication>password-cleartext</authentication>
        #       <username>%EMAILADDRESS%</username>
        #     </outgoingServer>

        smtp = configs[0]
        self.assertEqual('smtp.cesky-hosting.cz', smtp.hostname)
        self.assertEqual(465, smtp.port)
        self.assertEqual('SSL', smtp.socket_type)
        self.assertEqual(1, len(smtp.authentications))
        self.assertEqual('password-cleartext', smtp.authentications[0])
        self.assertEqual('%EMAILADDRESS%', smtp.username)

        #     <outgoingServer type="smtp">
        #       <hostname>smtp.cesky-hosting.cz</hostname>
        #       <port>587</port>
        #       <socketType>STARTTLS</socketType>
        #       <authentication>password-cleartext</authentication>
        #       <username>%EMAILADDRESS%</username>
        #     </outgoingServer>

        smtp = configs[1]
        self.assertEqual('smtp.cesky-hosting.cz', smtp.hostname)
        self.assertEqual(587, smtp.port)
        self.assertEqual('STARTTLS', smtp.socket_type)
        self.assertEqual(1, len(smtp.authentications))
        self.assertEqual('password-cleartext', smtp.authentications[0])
        self.assertEqual('%EMAILADDRESS%', smtp.username)

        #     <outgoingServer type="smtp">
        #       <hostname>smtp.cesky-hosting.cz</hostname>
        #       <port>25</port>
        #       <socketType>STARTTLS</socketType>
        #       <authentication>password-cleartext</authentication>
        #       <username>%EMAILADDRESS%</username>
        #     </outgoingServer>

        smtp = configs[2]
        self.assertEqual('smtp.cesky-hosting.cz', smtp.hostname)
        self.assertEqual(25, smtp.port)
        self.assertEqual('STARTTLS', smtp.socket_type)
        self.assertEqual(1, len(smtp.authentications))
        self.assertEqual('password-cleartext', smtp.authentications[0])
        self.assertEqual('%EMAILADDRESS%', smtp.username)

        # --------------------------------------------------------------------

        #     <outgoingServer type="smtp">
        #       <hostname>smtp.mail.yahoo.com</hostname>
        #       <port>465</port>
        #       <socketType>SSL</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>OAuth2</authentication>
        #       <authentication>password-cleartext</authentication>
        #     </outgoingServer>

        isp_name = 'yahoo.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_smtp_configs()
        smtp = configs[0]

        self.assertEqual(2, len(smtp.authentications))
        self.assertEqual('OAuth2', smtp.authentications[0])
        self.assertEqual('password-cleartext', smtp.authentications[1])

    def test_pop3_content(self):

        # --------------------------------------------------------------------

        isp_name = 'uymail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_pop3_configs()

        #     <incomingServer type="pop3">
        #       <hostname>pop.mail.com</hostname>
        #       <port>995</port>
        #       <socketType>SSL</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        pop3 = configs[0]
        self.assertEqual('pop.mail.com', pop3.hostname)
        self.assertEqual(995, pop3.port)
        self.assertEqual('SSL', pop3.socket_type)
        self.assertEqual('%EMAILADDRESS%', pop3.username)
        self.assertEqual(1, len(pop3.authentications))
        self.assertEqual('password-cleartext', pop3.authentications[0])

        #     <incomingServer type="pop3">
        #       <hostname>pop.mail.com</hostname>
        #       <port>110</port>
        #       <socketType>STARTTLS</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        pop3 = configs[1]
        self.assertEqual('pop.mail.com', pop3.hostname)
        self.assertEqual(110, pop3.port)
        self.assertEqual('STARTTLS', pop3.socket_type)
        self.assertEqual('%EMAILADDRESS%', pop3.username)
        self.assertEqual(1, len(pop3.authentications))
        self.assertEqual('password-cleartext', pop3.authentications[0])

        # --------------------------------------------------------------------

        #     <incomingServer type="pop3">
        #       <hostname>pop.mail.yahoo.com</hostname>
        #       <port>995</port>
        #       <socketType>SSL</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>OAuth2</authentication>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        isp_name = 'yahoo.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_pop3_configs()
        pop3 = configs[0]

        self.assertEqual(2, len(pop3.authentications))
        self.assertEqual('OAuth2', pop3.authentications[0])
        self.assertEqual('password-cleartext', pop3.authentications[1])

    def test_imap_content(self):

        # --------------------------------------------------------------------

        isp_name = 'uymail.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_imap_configs()

        #     <incomingServer type="imap">
        #       <hostname>imap.mail.com</hostname>
        #       <port>993</port>
        #       <socketType>SSL</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        imap = configs[0]
        self.assertEqual('imap.mail.com', imap.hostname)
        self.assertEqual(993, imap.port)
        self.assertEqual('SSL', imap.socket_type)
        self.assertEqual('%EMAILADDRESS%', imap.username)
        self.assertEqual(1, len(imap.authentications))
        self.assertEqual('password-cleartext', imap.authentications[0])

        #     <incomingServer type="imap">
        #       <hostname>imap.mail.com</hostname>
        #       <port>143</port>
        #       <socketType>STARTTLS</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        imap = configs[1]
        self.assertEqual('imap.mail.com', imap.hostname)
        self.assertEqual(143, imap.port)
        self.assertEqual('STARTTLS', imap.socket_type)
        self.assertEqual('%EMAILADDRESS%', imap.username)
        self.assertEqual(1, len(imap.authentications))
        self.assertEqual('password-cleartext', imap.authentications[0])

        # --------------------------------------------------------------------

        #     <incomingServer type="imap">
        #       <hostname>imap.mail.yahoo.com</hostname>
        #       <port>993</port>
        #       <socketType>SSL</socketType>
        #       <username>%EMAILADDRESS%</username>
        #       <authentication>OAuth2</authentication>
        #       <authentication>password-cleartext</authentication>
        #     </incomingServer>

        isp_name = 'yahoo.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())
        configs = isp.get_imap_configs()
        imap = configs[0]

        self.assertEqual(2, len(imap.authentications))
        self.assertEqual('OAuth2', imap.authentications[0])
        self.assertEqual('password-cleartext', imap.authentications[1])

    def test_domains(self):

        #     <domain>yahoo.com</domain>
        #     <domain>yahoo.de</domain>
        #     <domain>yahoo.it</domain>
        #     <domain>yahoo.fr</domain>
        #     <domain>yahoo.es</domain>
        #     <domain>yahoo.se</domain>
        #     <domain>yahoo.co.uk</domain>
        #     <domain>yahoo.co.nz</domain>
        #     <domain>yahoo.com.au</domain>
        #     <domain>yahoo.com.ar</domain>
        #     <domain>yahoo.com.br</domain>
        #     <domain>yahoo.com.mx</domain>
        #     <domain>ymail.com</domain>
        #     <domain>rocketmail.com</domain>
        #     <domain>yahoodns.net</domain>

        isp_name = 'yahoo.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())

        self.assertEqual(15, len(isp.get_provider_description().domains))
        self.assertEqual([
            'yahoo.com',
            'yahoo.de',
            'yahoo.it',
            'yahoo.fr',
            'yahoo.es',
            'yahoo.se',
            'yahoo.co.uk',
            'yahoo.co.nz',
            'yahoo.com.au',
            'yahoo.com.ar',
            'yahoo.com.br',
            'yahoo.com.mx',
            'ymail.com',
            'rocketmail.com',
            'yahoodns.net'
        ], isp.get_provider_description().domains)

    def test_provider_data(self):

        #     <displayName>Yahoo! Mail</displayName>
        #     <displayShortName>Yahoo</displayShortName>

        isp_name = 'yahoo.com.xml'
        isp_xml_path = os.path.join(self.data_path, isp_name)
        # noinspection PyUnusedLocal
        isp: Isp
        with open(isp_xml_path, 'r') as fd:
            isp = Isp(fd.read())

        self.assertEqual('Yahoo! Mail', isp.get_provider_description().display_name)
        self.assertEqual('Yahoo', isp.get_provider_description().display_short_name)

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
