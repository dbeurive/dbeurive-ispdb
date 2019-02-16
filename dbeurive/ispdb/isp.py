# This is for quick testing
if '__main__' == __name__:
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from xml.dom import minidom
from dbeurive.ispdb.provider import Provider
from dbeurive.ispdb.imap import Imap
from dbeurive.ispdb.pop3 import Pop3
from dbeurive.ispdb.smtp import Smtp
from typing import Union

class Isp:

    def __init__(self, in_xml: str):

        self._has_imap = False
        self._has_smtp = False
        self._has_pop3 = False
        self._provider: Provider = Provider()
        self._imap: Imap = Imap()
        self._pop3: Pop3 = Pop3()
        self._smtp: Smtp = Smtp()

        doc = minidom.parseString(in_xml)
        element_incoming_configurations: minidom.NodeList = doc.getElementsByTagName('incomingServer')
        element_outgoing_configurations: minidom.NodeList = doc.getElementsByTagName('outgoingServer')

        element_email_provider: minidom.Element = doc.getElementsByTagName('emailProvider')[0]
        self._init_provider(element_email_provider)

        element_imap_configuration = self._get_element_by_tag_value(element_incoming_configurations, 'type', 'imap')
        if element_imap_configuration is not None:
            self._has_imap = True
            self._init_imap(element_imap_configuration)

        element_pop3_configuration = self._get_element_by_tag_value(element_incoming_configurations, 'type', 'pop3')
        if element_pop3_configuration is not None:
            self._has_pop3 = True
            self._init_pop3(element_pop3_configuration)

        element_smtp_configuration = self._get_element_by_tag_value(element_outgoing_configurations, 'type', 'smtp')
        if element_smtp_configuration is not None:
            self._has_smtp = True
            self._init_smtp(element_smtp_configuration)

    def support_imap(self) -> bool:
        return self._has_imap

    def support_pop3(self) -> bool:
        return self._has_pop3

    def support_smtp(self) -> bool:
        return self._has_smtp

    def get_provider_description(self) -> Provider:
        return self._provider

    def get_imap_config(self) -> Union[None, Imap]:
        if self.support_imap():
            return self._imap
        else:
            return None

    def get_pop3_config(self) -> Union[None, Pop3]:
        if self.support_pop3():
            return self._pop3
        else:
            return None

    def get_smtp_config(self) -> Union[None, Smtp]:
        if self.support_smtp():
            return self._smtp
        else:
            return None


    def _init_provider(self, configuration: minidom.Element) -> None:
        self._provider.id = configuration.getAttribute('id')

        domains: minidom.NodeList = configuration.getElementsByTagName('domain')
        self._provider.domains = map(lambda x: self._get_text_from_single_text_element(x), domains)

        display_name: minidom.NodeList = configuration.getElementsByTagName('displayName')
        assert 1 == len(display_name)
        self._provider.display_name = self._get_text_from_single_text_element(display_name[0])

        display_short_name: minidom.NodeList = configuration.getElementsByTagName('displayShortName')
        assert 1 == len(display_short_name)
        self._provider.display_short_name = self._get_text_from_single_text_element(display_short_name[0])

    def _init_imap(self, configuration: minidom.Element) -> None:
        hostname: minidom.NodeList = configuration.getElementsByTagName('hostname')
        assert 1 == len(hostname)
        self._imap.hostname = self._get_text_from_single_text_element(hostname[0])

        port: minidom.NodeList = configuration.getElementsByTagName('port')
        assert 1 == len(port)
        self._imap.port = int(self._get_text_from_single_text_element(port[0]))

        socket_type = configuration.getElementsByTagName('socketType')
        assert 1 == len(socket_type)
        self._imap.socket_type = self._get_text_from_single_text_element(socket_type[0])

        username = configuration.getElementsByTagName('username')
        assert 1 == len(username)
        self._imap.username = self._get_text_from_single_text_element(username[0])

        authentications = configuration.getElementsByTagName('authentication')
        self._imap.authentications = map(lambda x: self._get_text_from_single_text_element(x), authentications)

    def _init_pop3(self, configuration: minidom.Element) -> None:
        hostname: minidom.NodeList = configuration.getElementsByTagName('hostname')
        assert 1 == len(hostname)
        self._pop3.hostname = self._get_text_from_single_text_element(hostname[0])

        port: minidom.NodeList = configuration.getElementsByTagName('port')
        assert 1 == len(port)
        self._pop3.port = int(self._get_text_from_single_text_element(port[0]))

        socket_type = configuration.getElementsByTagName('socketType')
        assert 1 == len(socket_type)
        self._pop3.socket_type = self._get_text_from_single_text_element(socket_type[0])

        username = configuration.getElementsByTagName('username')
        assert 1 == len(username)
        self._pop3.username = self._get_text_from_single_text_element(username[0])

        authentications = configuration.getElementsByTagName('authentication')
        self._pop3.authentications = map(lambda x: self._get_text_from_single_text_element(x), authentications)

    def _init_smtp(self, configuration: minidom.Element) -> None:
        hostname: minidom.NodeList = configuration.getElementsByTagName('hostname')
        assert 1 == len(hostname)
        self._smtp.hostname = self._get_text_from_single_text_element(hostname[0])

        port: minidom.NodeList = configuration.getElementsByTagName('port')
        assert 1 == len(port)
        self._smtp.port = int(self._get_text_from_single_text_element(port[0]))

        socket_type = configuration.getElementsByTagName('socketType')
        assert 1 == len(socket_type)
        self._smtp.socket_type = self._get_text_from_single_text_element(socket_type[0])

        username = configuration.getElementsByTagName('username')
        assert 1 == len(username)
        self._smtp.username = self._get_text_from_single_text_element(username[0])

        authentications = configuration.getElementsByTagName('authentication')
        self._smtp.authentications = map(lambda x: self._get_text_from_single_text_element(x), authentications)




    @staticmethod
    def _get_text_from_single_text_element(element: minidom.Element) -> str:
        children = element.childNodes
        assert 1 == len(children)
        child: minidom.Text = children[0]
        assert minidom.Node.TEXT_NODE == child.nodeType
        return child.data

    @staticmethod
    def _get_element_by_tag_value(nodes: minidom.NodeList, attr_name:str, attr_value:str) -> Union[None, minidom.Element] :
        # noinspection PyUnusedLocal
        element: minidom.Element
        for element in nodes:
            assert element.hasAttribute(attr_name)
            value: str = element.getAttribute(attr_name)
            if value == attr_value:
                return element
        return None







# -----------------------------------------------------------------
# Quick test
# -----------------------------------------------------------------

if '__main__' == __name__:

    xml = '''<clientConfig version="1.1">
      <emailProvider id="googlemail.com">
        <domain>gmail.com</domain>
        <domain>googlemail.com</domain>
        <!-- MX, for Google Apps -->
        <domain>google.com</domain>
        <!-- HACK. Only add ISPs with 100000+ users here -->
        <domain>jazztel.es</domain>
        <displayName>Google Mail</displayName>
        <displayShortName>GMail</displayShortName>
        <incomingServer type="imap">
          <hostname>imap.gmail.com</hostname>
          <port>993</port>
          <socketType>SSL</socketType>
          <username>%EMAILADDRESS%</username>
          <authentication>OAuth2</authentication>
          <authentication>password-cleartext</authentication>
        </incomingServer>
        <incomingServer type="pop3">
          <hostname>pop.gmail.com</hostname>
          <port>995</port>
          <socketType>SSL</socketType>
          <username>%EMAILADDRESS%</username>
          <authentication>password-cleartext</authentication>
          <pop3>
            <leaveMessagesOnServer>true</leaveMessagesOnServer>
          </pop3>
        </incomingServer>
        <outgoingServer type="smtp">
          <hostname>smtp.gmail.com</hostname>
          <port>465</port>
          <socketType>SSL</socketType>
          <username>%EMAILADDRESS%</username>
          <authentication>OAuth2</authentication>
          <authentication>password-cleartext</authentication>
        </outgoingServer>
        <enable visiturl="https://mail.google.com/mail/?ui=2&amp;shva=1#settings/fwdandpop">
          <instruction>You need to enable IMAP access</instruction>
        </enable>
        <documentation url="http://mail.google.com/support/bin/answer.py?answer=13273">
          <descr>How to enable IMAP/POP3 in GMail</descr>
        </documentation>
        <documentation url="http://mail.google.com/support/bin/topic.py?topic=12806">
          <descr>How to configure email clients for IMAP</descr>
        </documentation>
        <documentation url="http://mail.google.com/support/bin/topic.py?topic=12805">
          <descr>How to configure email clients for POP3</descr>
        </documentation>
        <documentation url="http://mail.google.com/support/bin/answer.py?answer=86399">
          <descr>How to configure TB 2.0 for POP3</descr>
        </documentation>
      </emailProvider>
    
      <webMail>
        <loginPage url="https://accounts.google.com/ServiceLogin?service=mail&amp;continue=http://mail.google.com/mail/"/>
        <loginPageInfo url="https://accounts.google.com/ServiceLogin?service=mail&amp;continue=http://mail.google.com/mail/">
          <username>%EMAILADDRESS%</username>
          <usernameField id="Email"/>
          <passwordField id="Passwd"/>
          <loginButton id="signIn"/>
        </loginPageInfo>
      </webMail>
    
    </clientConfig>
    '''

    domain = Isp(xml)