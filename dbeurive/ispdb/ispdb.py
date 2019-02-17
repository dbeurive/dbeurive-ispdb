# This is for quick testing

if '__main__' == __name__:
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

import urllib.request
import cgi
from typing import Union, Dict, List
from pprint import pprint
from http.client import HTTPResponse
from http.client import HTTPMessage
from collections import Mapping
from dbeurive.ispdb.web.parser import Parser
from dbeurive.ispdb.web.isp import Isp as IspRef



class Ispdb:
    ISPDB_URL='https://autoconfig.thunderbird.net/v1.1/'

    def get_isp_list(self) -> List[IspRef]:
        response: HTTPResponse = urllib.request.urlopen(self.ISPDB_URL)
        charset = self._get_charset(response)
        html  = response.read().decode(charset)
        parser = Parser()
        parser.feed(html)
        isps = parser.get_isps()
        return isps

    def get_isp(self, isp_name: str):
        response: HTTPResponse = urllib.request.urlopen(f'{self.ISPDB_URL}/{isp_name}')
        charset = self._get_charset(response)
        xml = response.read().decode(charset)
        pass

    @staticmethod
    def _get_charset(response: HTTPResponse) -> Union[str, None]:
        h: HTTPMessage = response.info()
        content_type = h.get('Content-Type')
        params = cgi.parse_header(content_type)
        # noinspection PyUnusedLocal
        param: Union[Dict[str, str], str]
        for param in params:
            if isinstance(param, Mapping):
                if 'charset' in param:
                    return param['charset']
        return None


# -----------------------------------------------------------------
# Quick test
# -----------------------------------------------------------------

if '__main__' == __name__:

    requester = Ispdb()
    r = requester.get_isp_list()

    pprint(r)

