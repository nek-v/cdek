# -*- coding: utf-8 -*-
import datetime
import json
from typing import Dict, List, Optional
from urllib.parse import urlencode

import requests
from boltons.iterutils import remap
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from .entities import DeliveryRequest, PreAlert


class CDEKClient:
    PROD_BASE_URI = "https://api.cdek.ru/v2"

    TEST_BASE_URI = "https://api.edu.cdek.ru/v2"

    CITIES_URI = "/location/cities"

    CODE_CALCULATOR_URI = "/calculator/tariff"

    ORDERS_URI = "/orders"

    PREALERT_URI = "/prealert"

    TOKEN_URI = "/oauth/token?grant_type=client_credentials"

    def __init__(self, client_id, client_secret, prod_environment):
        self.client_secret = client_secret
        self.client_id = client_id
        if not prod_environment:
            self.url = self.TEST_BASE_URI
        else:
            self.url = self.PROD_BASE_URI

    def get_shipping_cost_by_tariff_code(
        self,
        packages: List[dict],
        tariff_code: int,
        from_location: List[dict],
        to_location: List[dict],
        date: datetime = None,
        order_type: Optional[int] = None,
        currency: Optional[int] = None,
        services: Optional[List[dict]] = None,
    ):
        params = {
            "packages": packages,
            "date": date,
            "order_type": order_type,
            "currency": currency,
            "tariff_code": tariff_code,
            "from_location": from_location,
            "to_location": to_location,
            "services": services,
        }

        url = self.url + self.CODE_CALCULATOR_URI
        response = self._request(url, data=json.dumps(params))
        return response.json()

    def create_orders(self, delivery_request: DeliveryRequest):
        url = self.url + self.ORDERS_URI
        data = delivery_request.to_json()
        response = self._request(url, data=data)
        return response.json()

    def info_orders(
        self,
        uuid: Optional[str] = None,
        cdek_number: Optional[str] = None,
        im_number: Optional[str] = None,
    ):
        if uuid:
            url = self.url + self.ORDERS_URI + "/" + uuid
        elif cdek_number:
            url = self.url + self.ORDERS_URI + "?cdek_number=" + cdek_number
        elif im_number:
            url = self.url + self.ORDERS_URI + "?im_number=" + im_number
        else:
            raise ValueError("No query parameters defined!")
        response = self._request(url, data={}, method="GET")
        return response.json()

    def delete_orders(self, uuid: str):
        url = self.url + self.ORDERS_URI + "/" + uuid
        response = self._request(url, data={}, method="DELETE")
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
        lang: Optional[str] = None,
    ):
        params = {
            "country_codes": country_codes,
            "region_code": region_code,
            "fias_guid": fias_guid,
            "postal_code": postal_code,
            "code": code,
            "city": city,
            "size": size,
            "page": page,
            "lang": lang,
        }
        url = self.url + self.CITIES_URI
        response = self._request(url, data=params, method="GET")
        return response.json()

    def create_prealerts(self, pre_alert: PreAlert):

        url = self.url + self.PREALERT_URI
        response = self._request(
            url, data=json.dumps(pre_alert.pre_alert_element)
        )
        return response.json()

    def _request(
        self, url: str, data: Dict, stream: bool = False, method: str = "POST"
    ):
        token = self._fetch_token()
        headers = {
            "Authorization": "Bearer " + token,
            "Content-type": "application/json",
        }
        if isinstance(data, dict):
            data = remap(data, lambda p, k, v: v is not None)
        if method == "GET":
            url = f"{url}?{urlencode(data)}"
            response = requests.get(url, stream=stream, headers=headers)
        elif method == "POST":
            response = requests.post(
                url, data=data, stream=stream, headers=headers
            )
        elif method == "DELETE":
            response = requests.delete(url, stream=stream, headers=headers)
        else:
            raise NotImplementedError(f'Unknown method "{method}"')
        response.raise_for_status()
        return response

    def _fetch_token(self):
        url = self.url + self.TOKEN_URI
        oauth_client = BackendApplicationClient(client_id=self.client_id)
        oauth_session = OAuth2Session(client=oauth_client)
        token = oauth_session.fetch_token(
            token_url=url,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return OAuth2Session(
            client_id=self.client_id, token=token
        ).access_token
