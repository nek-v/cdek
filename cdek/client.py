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


class CDEKClient:
    BASE_URI = 'https://api.edu.cdek.ru/v2'

    CITIES_URI = '/location/cities'

    CODE_CALCULATOR_URI = '/calculator/tariff'

    ORDERS_URI = '/orders'

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
            packages: List[dict],
            tariff_code: int,
            from_location: List[dict],
            to_location: List[dict],
            date: datetime = None,
            type: Optional[int] = None,
            currency: Optional[int] = None,
            services: Optional[List[dict]] = None,
    ):
        params = {
            'packages': packages,
            'date': date,
            'type': type,
            'currency': currency,
            'tariff_code': tariff_code,
            'from_location': from_location,
            'to_location': to_location,
            'services': services
        }

        url = self.BASE_URI + self.CODE_CALCULATOR_URI
        response = self._request(url, data=json.dumps(params))
        return response.json()

    def create_orders(
            self,
            tariff_code: int,
            recipient: List[dict],
            packages: List[dict],
            type: Optional[int] = None,
            number: Optional[str] = None,
            comment: Optional[str] = None,
            developer_key: Optional[str] = None,
            shipment_point: Optional[str] = None,
            delivery_point: Optional[str] = None,
            date_invoice: datetime = None,
            shipper_name: Optional[str] = None,
            shipper_address: Optional[str] = None,
            delivery_recipient_cost: Optional[List[dict]] = None,
            delivery_recipient_cost_adv: Optional[List[dict]] = None,
            sender: Optional[List[dict]] = None,
            seller: Optional[List[dict]] = None,
            from_location: Optional[List[dict]] = None,
            to_location: Optional[List[dict]] = None,
            services: Optional[List[dict]] = None,
            print: Optional[str] = None
    ):
        params = {
            'tariff_code': tariff_code,
            'recipient': recipient,
            'packages': packages,
            'type': type,
            'number': number,
            'comment': comment,
            'developer_key': developer_key,
            'shipment_point': shipment_point,
            'delivery_point': delivery_point,
            'date_invoice': date_invoice,
            'shipper_name': shipper_name,
            'shipper_address': shipper_address,
            'delivery_recipient_cost': delivery_recipient_cost,
            'delivery_recipient_cost_adv': delivery_recipient_cost_adv,
            'sender': sender,
            'seller': seller,
            'from_location': from_location,
            'to_location': to_location,
            'service': services,
            'print': print
        }

        url = self.BASE_URI + self.ORDERS_URI
        response = self._request(url, data=json.dumps(params))
        return response.json()

    def get_cities(
            self,
            country_codes: Optional[str] = None,
            region_code: Optional[int] = None,
            fias_guid: Optional[str] = None,
            postal_code: Optional[str] = None,
            code: Optional[int] = None,
            city: Optional[str] = None,
            size: Optional[int] = None,
            page: Optional[int] = None,
            lang: Optional[str] = None
    ):
        params = {
            'country_codes': country_codes,
            'region_code': region_code,
            'fias_guid': fias_guid,
            'postal_code': postal_code,
            'code': code,
            'city': city,
            'size': size,
            'page': page,
            'lang': lang
        }
        url = self.BASE_URI + self.CITIES_URI
        response = self._request(url, data=params, method='GET')
        return response.json()

    def _request(self, url: str, data: Dict, stream: bool = False, method: str = 'POST'):
        token = self._fetch_token()
        headers = {'Authorization': 'Bearer ' + token, 'Content-type': 'application/json'}
        if isinstance(data, dict):
            data = remap(data, lambda p, k, v: v is not None)
        if method == 'GET':
            url = f'{url}?{urlencode(data)}'
            response = requests.get(
                url, stream=stream, headers=headers
            )
        elif method == 'POST':
            response = requests.post(url, data=data, stream=stream, headers=headers)
        else:
            raise NotImplementedError(f'Unknown method "{method}"')
        response.raise_for_status()
        return response

    def _fetch_token(self):
        oauth_client = BackendApplicationClient(client_id=self.client_id)
        oauth_session = OAuth2Session(client=oauth_client)
        token = oauth_session.fetch_token(token_url=self.url,
                                          client_id=self.client_id,
                                          client_secret=self.client_secret)
        return OAuth2Session(client_id=self.client_id, token=token).access_token
