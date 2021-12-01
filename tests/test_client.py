# -*- coding: utf-8 -*-
import pytest
from contextlib import ExitStack as does_not_raise
from typing import Dict

from cdek.client import CDEKClient


@pytest.fixture
def cdek_client():
    return CDEKClient(
        client_id='EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
        client_secret='PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',
        prod_environment=False,
    )


def test__fetch_token(cdek_client: CDEKClient):
    assert cdek_client._fetch_token()


@pytest.mark.parametrize('tariff,expectation', [
    pytest.param({'tariff_code': 1}, does_not_raise(), id='Single tariff'),
    pytest.param({}, pytest.raises(AttributeError), marks=pytest.mark.xfail, id='Without tariff')
])
def test_get_shipping_cost_by_tariff_code(cdek_client: CDEKClient, tariff: Dict,
                                          expectation):
    with expectation:
        shipping_costs = cdek_client.get_shipping_cost_by_tariff_code(
            from_location={'code': 270},
            to_location={'code': 44},
            packages=[
                {'weight': 100, 'length': 10, 'width': 7, 'height': 5},
                {'weight': 100},
            ],
            services=[{'code': 'BUBBLE_WRAP', 'parameter': 2}],
            **tariff
        )

        assert shipping_costs
        assert 'error' not in shipping_costs
        assert 'weight_calc' in shipping_costs
        weight_calc = shipping_costs['weight_calc']
        assert weight_calc == 200


@pytest.mark.parametrize('type,expectation', [
    pytest.param({'type': 1}, does_not_raise(), id='Type Online Store'),
    pytest.param({'type': 2}, pytest.raises(AttributeError), marks=pytest.mark.xfail, id='Type Delivery')
])
def test_order_creation_for_os(cdek_client: CDEKClient, type: Dict,
                              expectation):
    with expectation:
        send_orders = cdek_client.create_orders(
            from_location=
            {
                "code": "44",
                "fias_guid": "",
                "postal_code": "",
                "longitude": "",
                "latitude": "",
                "country_code": "",
                "region": "",
                "sub_region": "",
                "city": "Москва",
                "kladr_code": "",
                "address": "пр. Ленинградский, д.4"
            },
            to_location={
                "code": "270",
                "fias_guid": "",
                "postal_code": "",
                "longitude": "",
                "latitude": "",
                "country_code": "",
                "region": "",
                "sub_region": "",
                "city": "Новосибирск",
                "kladr_code": "",
                "address": "ул. Блюхера, 32"
            },
            packages=[{
                "number": "bar-001",
                "comment": "Упаковка",
                "height": 10,
                "items": [{
                    "ware_key": "00055",
                    "payment": {
                        "value": 3000
                    },
                    "name": "Товар",
                    "cost": 300,
                    "amount": 2,
                    "weight": 700,
                    "url": "www.item.ru"
                }],
                "length": 10,
                "weight": 4000,
                "width": 10
            }],
            recipient={
                "name": "Иванов Иван",
                "phones": [{
                    "number": "+79134637228"
                }]
            },
            tariff_code=139,
            **type
        )

        assert send_orders
        assert len(send_orders) == 2
        assert 'entity' in send_orders
        assert 'requests' in send_orders
        state = send_orders['requests'][0]['state']
        assert state == 'ACCEPTED'


@pytest.mark.parametrize('type,expectation', [
    pytest.param({'type': 2}, does_not_raise(), id='Type Delivery'),
    pytest.param({'type': 1}, pytest.raises(AttributeError), marks=pytest.mark.xfail, id='Type Online Store')
])
def test_order_creation_for_delivery(cdek_client: CDEKClient, type: Dict,
                                    expectation):
    with expectation:
        send_orders = cdek_client.create_orders(
            tariff_code=119,
            shipment_point="MSK67",
            sender={
                "company": "Компания",
                "name": "Петров Петр",
                "email": "msk@cdek.ru",
                "phones": [
                    {
                        "number": "+79134000101"
                    }
                ]
            },
            recipient={
                "company": "Иванов Иван",
                "name": "Иванов Иван",
                "passport_series": "5008",
                "passport_number": "345123",
                "passport_date_of_issue": "2019-03-12",
                "passport_organization": "ОВД Москвы",
                "tin": "123546789",
                "email": "email@gmail.com",
                "phones": [
                    {
                        "number": "+79134000404"
                    }
                ]
            },
            to_location={
                "code": "44",
                "fias_guid": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
                "postal_code": "109004",
                "longitude": 37.6204,
                "latitude": 55.754,
                "country_code": "RU",
                "region": "Москва",
                "sub_region": "Москва",
                "city": "Москва",
                "kladr_code": "7700000000000",
                "address": "ул. Блюхера, 32"
            },
            services=[
                {
                    "code": "INSURANCE",
                    "parameter": "3000"
                }
            ],
            packages=[
                {
                    "number": "bar-001",
                    "weight": "1000",
                    "length": 10,
                    "width": 140,
                    "height": 140,
                    "comment": "Test package"
                }
            ],
            **type
        )

        assert send_orders
        assert len(send_orders) == 2
        assert 'entity' in send_orders
        assert 'requests' in send_orders
        state = send_orders['requests'][0]['state']
        assert state == 'ACCEPTED'

def test_get_cities(cdek_client: CDEKClient):
    cities = cdek_client.get_cities(region_code=27,	size=1)

    assert cities
    assert cities[0]['country_code'] == 'RU'
    assert cities[0]['region'] == 'Башкортостан респ.'