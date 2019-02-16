# This is for quick testing
if '__main__' == __name__:
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir))

import urllib.request
from typing import Union, Dict, Any
from pprint import pprint
from http.client import HTTPResponse
from http.client import HTTPMessage
import cgi
from collections import Mapping
import html.parser

class Ispdb:
    ISPDB_URL='https://autoconfig.thunderbird.net/v1.1'

    def get_isp_list(self) -> str:
        response: HTTPResponse = urllib.request.urlopen(self.ISPDB_URL)
        charset = self._get_charset(response)
        return response.read().decode(charset)

    def get_isp(self, isp_name: str):
        urllib.request.urlopen(f'{self.ISPDB_URL}/{isp_name}')
        pass

    @staticmethod
    def _get_charset(response: HTTPResponse) -> Union[str, None]:
        h: HTTPMessage = response.info()
        content_type = h.get('Content-Type')
        params = cgi.parse_header(content_type)
        # noinspection PyUnusedLocal
        param: Union[Dict[Any, Any], Any]
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

