from __future__ import with_statement
import os
import sys
import re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

from typing import Mapping, List, Union
from dbeurive.ispdb.isp import Isp
from dbeurive.ispdb.smtp import Smtp
from dbeurive.ispdb.pop3 import Pop3
from dbeurive.ispdb.imap import Imap


KEY_SMTP = 'smtp'
KEY_POP3 = 'pop3'
KEY_IMAP = 'imap'

data_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')

xmlreg = re.compile('.xml$')
xml_files = [f for f in os.listdir(data_dir_path) if
            os.path.isfile(os.path.join(data_dir_path, f)) and xmlreg.search(f) is not None]

data_by_name: Mapping[str, Mapping[str, int]] = {KEY_IMAP: {}, KEY_POP3: {}, KEY_SMTP: {}}
data_by_count: Mapping[str, Mapping[int, List[str]]] = {KEY_IMAP: {}, KEY_POP3: {}, KEY_SMTP: {}}
valid: List[str] = []
invalid: List[str] = []
auth_smtp: List[str] = []
auth_imap: List[str] = []
auth_pop3: List[str] = []

for xml_file in xml_files:
    xml_path = os.path.join(data_dir_path, xml_file)
    xml: str = None
    try:
        with open(xml_path, 'r') as fd:
            xml = fd.read()
    except EnvironmentError as e:
        print(f'ERROR: cannot read the file "{xml_file}": {e.strerror}')
        exit(1)
    isp = Isp(xml)

    if isp.is_valid():
        valid.append(xml_file)
    else:
        invalid.append(xml_file)

    data_by_name[KEY_IMAP][xml_file] = isp.get_imap_configs_count()
    data_by_name[KEY_SMTP][xml_file] = isp.get_smtp_configs_count()
    data_by_name[KEY_POP3][xml_file] = isp.get_pop3_configs_count()

    if isp.get_imap_configs_count() not in data_by_count[KEY_IMAP]:
        data_by_count[KEY_IMAP][isp.get_imap_configs_count()] = []
    if isp.get_smtp_configs_count() not in data_by_count[KEY_SMTP]:
        data_by_count[KEY_SMTP][isp.get_smtp_configs_count()] = []
    if isp.get_pop3_configs_count() not in data_by_count[KEY_POP3]:
        data_by_count[KEY_POP3][isp.get_pop3_configs_count()] = []

    data_by_count[KEY_IMAP][isp.get_imap_configs_count()].append(xml_file)
    data_by_count[KEY_SMTP][isp.get_smtp_configs_count()].append(xml_file)
    data_by_count[KEY_POP3][isp.get_pop3_configs_count()].append(xml_file)

    config: Union[None, List[Imap]] = isp.get_imap_configs()
    if config is not None:
        for conf in isp.get_imap_configs():
            if len(conf.authentications) > 1:
                auth_imap.append(xml_file)

    config: Union[None, List[Smtp]] = isp.get_smtp_configs()
    if config is not None:
        for conf in isp.get_smtp_configs():
            if len(conf.authentications) > 1:
                auth_smtp.append(xml_file)

    config: Union[None, List[Pop3]] = isp.get_pop3_configs()
    if config is not None:
        for conf in isp.get_pop3_configs():
            if len(conf.authentications) > 1:
                auth_pop3.append(xml_file)


# Print lists of files for a given protocol and a given configuration count.

for protocol, counts in data_by_count.items():
    print(f"{protocol}:")
    count: Mapping[int, List[str]]
    for count, files in counts.items():
        print(f"\t{count}: {', '.join(files[0:3])}")
    print("")

# Print lists of valid and invalid files.

print(f'VALID: {", ".join(valid[0:3])}')
print(f'INVALID: {", ".join(invalid[0:3])}')
print("")

# Print lists of configurations that have more than one authentication method.

print(f'SMTP: {", ".join(auth_imap[0:3])}')
print(f'POP3: {", ".join(auth_pop3[0:3])}')
print(f'IMAP: {", ".join(auth_imap[0:3])}')
print("")