# This is for quick testing

if '__main__' == __name__:
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

import urllib.request
import cgi
from typing import Union, Dict, List, Tuple
from pprint import pprint
from http.client import HTTPResponse
from http.client import HTTPMessage
from collections import Mapping
from dbeurive.ispdb.web.parser import Parser
from dbeurive.ispdb.web.isp import Isp as IspRef



class Ispdb:
    ISPDB_URL='https://autoconfig.thunderbird.net/v1.1/'

    def get_isp_list(self) -> Tuple[str, List[IspRef]]:
        response: HTTPResponse = urllib.request.urlopen(self.ISPDB_URL)
        charset, found = self._get_charset(response)
        html_response = response.read().decode(charset)
        parser = Parser()
        parser.feed(html_response)
        isps_list = parser.get_isps()
        return html_response, isps_list

    def get_isp_raw_data(self, isp_name: str) -> str:
        response: HTTPResponse = urllib.request.urlopen(f'{self.ISPDB_URL}/{isp_name}')
        charset, found = self._get_charset(response)
        assert charset is not None
        xml_desc = response.read().decode(charset)
        return xml_desc

    def get_isps_raw_data(self) -> List[str]:
        ispdb_requester = Ispdb()
        html_response, isps_list = ispdb_requester.get_isp_list()
        list_result = []
        for isp in isps_list:
            xml_desc = self.get_isp_raw_data(isp.name)
            list_result.append(xml_desc)
        return list_result







    @staticmethod
    def _get_charset(response: HTTPResponse) -> Tuple[str, bool]:
        h: HTTPMessage = response.info()
        content_type = h.get('Content-Type')
        params = cgi.parse_header(content_type)
        # noinspection PyUnusedLocal
        param: Union[Dict[str, str], str]
        for param in params:
            if isinstance(param, Mapping):
                if 'charset' in param:
                    return param['charset'], True
        # @see https://www.w3.org/International/articles/http-charset/index
        return 'ISO-8859-1', False


# -----------------------------------------------------------------
# Quick test
# -----------------------------------------------------------------

if '__main__' == __name__:

    requester = Ispdb()
    html, isps = requester.get_isp_list()

    xml = requester.get_isp_raw_data('gmail.com')
    print(xml)

