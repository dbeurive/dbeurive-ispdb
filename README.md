# Description

This repository contains an API designed to get data from the [Mozilla ISP database](https://autoconfig.thunderbird.net/v1.1/).

# Prerequisites

This script needs Python version 3.6 or greater.

> We heavily use typing hint since it makes things clearer.

# Synopsis

> Please note that we use typing hint since it makes things clearer.

    from typing import Mapping, List, Union
    from dbeurive.ispdb.isp import Isp
    from dbeurive.ispdb.smtp import Smtp
    from dbeurive.ispdb.pop3 import Pop3
    from dbeurive.ispdb.imap import Imap
    from dbeurive.ispdb.web.webisp import WebIsp
    
    # Get the list of ISPs from the ISP database.
    #     - html: the content of the HTML file at "https://autoconfig.thunderbird.net/v1.1/".
    #     - isps: the list of ISPs.
    
    ispdb = Ispdb()
    # noinspection PyUnusedLocal
    html: str; isp: List[WebIsp]
    # noinspection PyRedeclaration
    html, isps = ispdb.get_isp_list()
    
    # Get data about a given ISP.
    #     - xml: the XML data as downloaded from the ISP database.
    
    xml = ispdb.get_isp_raw_data('alice.it.xml')

    # Extract data from the XML file previously downloaded.
    #     - smtp_configs: list of "Smtp" configurations (may be None).
    #     - imap_configs: list of "Imap" configurations (may be None).
    #     - pop3_configs: list of "Pop3" configurations (may be None).
    
    isp = Isp(xml)
    imap_config: Union[None, List[Imap]] = isp.get_imap_configs()
    smtp_config: Union[None, List[Smtp]] = isp.get_smtp_configs()
    pop3_config: Union[None, List[Pop3]] = isp.get_pop3_configs()

    # Get data from a configuration. For example, for the IMAP configuration.
    # We assume that "imap_config" contains at least one element !
    
    imap: Imap = imap_config[0]
    imap_auth_methods: List[str] = imap.authentications
    imap_hostname: str = imap.hostname
    imap_port: int = imap.port
    imap_socket_type: str = imap.socket_type
    imap_username: str = imap.username
    
    # You can do similar extractions for SMTP and POP3 configurations.
    
    # Get the list of domain names for the ISP.
    domains: List[str] = isp.get_provider_description().domains

    # Get the "display name" for the ISP.
    display_name: str = isp.get_provider_description().display_name
    
    # Get the "display short name" for the ISP.
    display_short_name: str = isp.get_provider_description().display_short_name

# Run the unit tests

    ./unittests.sh



