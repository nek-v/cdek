# -*- coding: utf-8 -*-

import datetime
from contextlib import ExitStack as does_not_raise
from typing import Dict

import pytest

from cdek.client import CDEKClient


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


def test_order_creation_for_os(cdek_client: CDEKClient, delivery_request):
    send_orders = cdek_client.create_orders(delivery_request)

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
                "phones": [{"number": "+79134000101"}]
            },
            recipient={
                "name": "Иванов Иван",
                "phones": [{"number": "+79130000000"}]
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
            services=[{"code": "INSURANCE", "parameter": "3000"}],
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


def test_delete_orders(cdek_client: CDEKClient):
    send_orders = cdek_client.create_orders(
        from_location=
        {
            "code": "44",
            "city": "Москва",
            "address": "пр. Ленинградский, д.4"
        },
        to_location={
            "code": "270",
            "city": "Новосибирск",
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
            "phones": [{"number": "+79134637228"}]
        },
        tariff_code=139, type=2)
    assert send_orders
    assert len(send_orders) == 2
    order = send_orders['entity']
    assert 'uuid' in order
    status = cdek_client.info_orders(uuid=order['uuid'])
    assert status
    assert 'entity' in status
    assert status['entity']['uuid'] == order['uuid']
    assert status['requests'][0]['type'] == 'CREATE'
    delete_request = cdek_client.delete_orders(uuid=status['entity']['uuid'])
    assert delete_request
    assert delete_request['entity']['uuid'] == status['entity']['uuid']
    assert delete_request['requests'][0]['type'] == 'DELETE'


def test_create_prealert(cdek_client: CDEKClient):
    send_orders = cdek_client.create_orders(
        from_location=
        {
            "code": "44",
            "city": "Москва",
            "address": "пр. Ленинградский, д.4"
        },
        to_location={
            "code": "270",
            "city": "Новосибирск",
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
            "phones": [{"number": "+79134637228"}]
        },
        tariff_code=139, type=1)
    assert send_orders
    assert len(send_orders) == 2
    order = send_orders['entity']
    assert 'uuid' in order
    planned_date = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S+0000')
    send_prealert = cdek_client.create_prealert(
        planned_date=planned_date,
        shipment_point='NSK27',
        orders=[{'uuid': order['uuid']}]
    )
    assert send_prealert
    assert send_prealert['entity']['uuid'] == order['uuid']
    assert send_prealert['requests'][0]['type'] == 'CREATE'


def test_get_cities(cdek_client: CDEKClient):
    cities = cdek_client.get_cities(region_code=27, size=1)

    assert cities
    assert cities[0]['country_code'] == 'RU'
    assert cities[0]['region'] == 'Башкортостан респ.'
