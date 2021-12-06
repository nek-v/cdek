# -*- coding: utf-8 -*-
from decimal import Decimal
from random import randint

import pytest

from cdek.client import CDEKClient
from cdek.entities import DeliveryRequest

delivery_type_list = [
    {
        'recipient_address': dict(code="270", city="Новосибирск", address="ул. Блюхера, 32"),
        'shipment_point': 'MSK67',
        'tariff_code': 138,
        'shipping_price': 300.0,
        'sender': None,
        'type': 1
    },
    {
        'recipient_address': dict(code="270", city="Новосибирск", address="ул. Блюхера, 32"),
        'shipment_point': 'MSK67',
        'tariff_code': 139,
        'shipping_price': 0,
        'sender': dict(company="Компания", name="Петров Петр", email="msk@cdek.ru",
                       phones=[{"number": "+79134000101"}]),
        'type': 2
    },
]


@pytest.fixture
def cdek_client():
    return CDEKClient(
        client_id='EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI',
        client_secret='PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG',
        prod_environment=False,
    )


@pytest.fixture(params=delivery_type_list, ids=[1, 2])
def delivery_type(request):
    return request.param


@pytest.fixture
def delivery_request(delivery_type):
    delivery_request_obj = DeliveryRequest()

    order = delivery_request_obj.add_order(
        type=delivery_type['type'],
        number=randint(100000, 1000000),
        tariff_code=delivery_type['tariff_code'],
        shipment_point=delivery_type['shipment_point'],
        recipient=dict(name='Иванов Иван Иванович', phones=[{'number': '+79999999999', }]),
        sender=delivery_type['sender']
    )

    delivery_request_obj.add_address(
        order, **delivery_type['recipient_address'])

    package = delivery_request_obj.add_package(
        order_element=order,
        length=10,
        width=10,
        height=10,
        number=str(randint(100000, 1000000)),
        weight=600
    )

    delivery_request_obj.add_item(
        package_element=package,
        name='test',
        amount=0,
        weight=500,
        cost=Decimal(1000),
        ware_key=str(randint(100000, 1000000)),
        # comment='Духи',
    )

    return delivery_request_obj
