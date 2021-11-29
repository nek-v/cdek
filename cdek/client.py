# -*- coding: utf-8 -*-

import datetime
import json
import requests
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from boltons.iterutils import remap
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


class CDEKClient():
    BASE_URI = 'https://api.edu.cdek.ru/v2'

    CODE_CALCULATOR_URI = '/calculator/tariff'

    PROD_TOKEN_URI = '/oauth/token?grant_type=client_credentials'

    TEST_TOKEN_URI = '/oauth/token?grant_type=client_credentials'

    def __init__(self, client_id, client_secret, prod_environment):
        self.client_secret = client_secret
        self.client_id = client_id
        if not prod_environment:
            self.url = self.BASE_URI + self.TEST_TOKEN_URI
        else:
            self.url = self.BASE_URI + self.PROD_TOKEN_URI

    def get_shipping_cost_by_tariff_code(
            self,
            packages: List[Dict],
            date: Optional[datetime] = None,
            type: Optional[int] = 1,
            currency: Optional[int] = 1,
            tariff_code: Optional[int] = None,
            from_location: List[dict] = None,
            to_location: List[dict] = None,
            services: List[Dict] = None
    ):
        today = datetime.date.today().isoformat()
        params = {}
        url = self.BASE_URI+self.CODE_CALCULATOR_URI
        response = self._request(url, data=json.dump(params))
        response.raise_for_status()
        return response.json()


    def _request(self, url: str, data: Dict, stream: bool = False) -> requests.Response:
        token = self._fetch_token()
        headers = {'Authorization': 'Bearer ' + token}
        if isinstance(data, dict):
            data = remap(data, lambda p, k, v: v is not None)
        url = self.BASE_URI + url
        response = requests.post(url, data=data, stream=stream, headers=headers)
        response.raise_for_status()
        return response

    def _fetch_token(self):
        oauth_client = BackendApplicationClient(client_id=self.client_id)
        oauth_session = OAuth2Session(client=oauth_client)
        token = oauth_session.fetch_token(token_url=self.url,
                                          client_id=self.client_id,
                                          client_secret=self.client_secret)
        return OAuth2Session(client_id=self.client_id, token=token).access_token
