# -*- coding: utf-8 -*-
import datetime
import json
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

import requests

class CDEKClient():

    def __init__(self, client_id, client_secret, prod_environment):
        self.client_secret = client_secret
        self.client_id = client_id
        self.prod_environment = prod_environment

    def _exec_request(self, url: str, data: Dict, method: str = 'POST',
                      stream: bool = False, **kwargs) -> requests.Response:
        if isinstance(data, dict):
            data = clean_dict(data)

        url = self._api_url + url

        if method == 'GET':
            response = requests.get(
                f'{url}?{urlencode(data)}', stream=stream, **kwargs,
            )
        elif method == 'POST':
            response = requests.post(url, data=data, stream=stream, **kwargs)
        else:
            raise NotImplementedError(f'Unknown method "{method}"')

        response.raise_for_status()

        return response