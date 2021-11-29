# -*- coding: utf-8 -*-

from cdek.client import CDEKClient


def _auth():
    return CDEKClient(
        client_id='EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
        client_secret='PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',
        prod_environment=False,
    )

def test__fetch_token():
    client = _auth()
    assert client._fetch_token()

def test_get_shipping_cost_by_tariff_code():
    client = _auth()
    response = client.get_shipping_cost_by_tariff_code
    return response
