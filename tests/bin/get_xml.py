# This script is used to get data from the Mozilla web site. Data includes:
#
#   - The HTML file that lists all the ISPs.
#   - All the XML files that contain the ISPs data.
#
# Usage:
#
#      python3 get_xml.py

from __future__ import with_statement
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

import time
from dbeurive.ispdb.ispdb import Ispdb
from dbeurive.ispdb.web.webisp import WebIsp
from typing import List

data_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'data')
list_html_path = os.path.join(data_dir_path, 'ispdb.html')

print(f"Path to the data directory: {data_dir_path}")
print(f"HTML document: {list_html_path}")

ispdb = Ispdb()
# noinspection PyUnusedLocal
html: str; isp: List[WebIsp]
# noinspection PyRedeclaration
html, isps = ispdb.get_isp_list()

# -----------------------------------------------------------------------------
# Save the HTML code of the index page.
# -----------------------------------------------------------------------------

try:
    with open(list_html_path, 'w') as fd:
        fd.write(html)
except EnvironmentError as e:
    print(f'ERROR: cannot write data into the file "{list_html_path}": {e.strerror}')
    exit(1)

# -----------------------------------------------------------------------------
# Get all the ISPs XML files.
# -----------------------------------------------------------------------------

isp: WebIsp
for isp in isps:
    xml_path = os.path.join(data_dir_path, f'{isp.name}.xml')
    print(f'Get data for "{isp.name}" -> {xml_path}')
    xml = ispdb.get_isp_raw_data(isp.name)
    try:
        with open(xml_path, 'w') as fd:
            fd.write(xml)
    except EnvironmentError as e:
        print(f'ERROR: cannot write data into the file "{xml_path}": {e.strerror}')
        exit(1)
    time.sleep(1)

