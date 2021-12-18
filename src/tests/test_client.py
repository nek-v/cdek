# -*- coding: utf-8 -*-
import datetime
from contextlib import ExitStack as does_not_raise
from typing import Dict

import pytest

from cdek.client import CDEKClient
from cdek.entities import PreAlert


def test__fetch_token(cdek_client: CDEKClient):
    assert cdek_client._fetch_token()


@pytest.mark.parametrize(
    "tariff,expectation",
    [
        pytest.param({"tariff_code": 1}, does_not_raise(), id="Single tariff"),
        pytest.param(
            {},
            pytest.raises(AttributeError),
            marks=pytest.mark.xfail,
            id="Without tariff",
        ),
    ],
)
def test_get_shipping_cost_by_tariff_code(
    cdek_client: CDEKClient, tariff: Dict, expectation
):
    with expectation:
        shipping_costs = cdek_client.get_shipping_cost_by_tariff_code(
            from_location={"code": 270},
            to_location={"code": 44},
            packages=[
                {"weight": 100, "length": 10, "width": 7, "height": 5},
                {"weight": 100},
            ],
            services=[{"code": "BUBBLE_WRAP", "parameter": 2}],
            **tariff
        )

        assert shipping_costs
        assert "error" not in shipping_costs
        assert "weight_calc" in shipping_costs
        weight_calc = shipping_costs["weight_calc"]
        assert weight_calc == 200


def test_order_creation(cdek_client: CDEKClient, delivery_request):
    send_orders = cdek_client.create_orders(delivery_request)

    assert send_orders
    assert len(send_orders) == 2
    assert "entity" in send_orders
    assert "requests" in send_orders
    state = send_orders["requests"][0]["state"]
    assert state == "ACCEPTED"


def test_info_orders(cdek_client: CDEKClient, delivery_request):
    send_orders = cdek_client.create_orders(delivery_request)

    assert send_orders
    assert len(send_orders) == 2
    order = send_orders["entity"]
    assert "uuid" in order
    status = cdek_client.info_orders(uuid=order["uuid"])
    assert status
    assert "entity" in status
    assert status["entity"]["uuid"] == order["uuid"]
    assert status["requests"][0]["type"] == "CREATE"


def test_delete_orders(cdek_client: CDEKClient, delivery_request):
    send_orders = cdek_client.create_orders(delivery_request)

    assert send_orders
    assert len(send_orders) == 2
    order = send_orders["entity"]
    assert "uuid" in order
    status = cdek_client.info_orders(uuid=order["uuid"])
    assert status
    assert "entity" in status
    assert status["entity"]["uuid"] == order["uuid"]
    assert status["requests"][0]["type"] == "CREATE"
    delete_request = cdek_client.delete_orders(uuid=status["entity"]["uuid"])
    assert delete_request
    assert delete_request["entity"]["uuid"] == status["entity"]["uuid"]
    assert delete_request["requests"][0]["type"] == "DELETE"


def test_get_cities(cdek_client: CDEKClient):
    cities = cdek_client.get_cities(region_code=27, size=1)

    assert cities
    assert cities[0]["country_code"] == "RU"
    assert cities[0]["region"] == "Башкортостан респ."


def test_create_prealerts(cdek_client: CDEKClient, delivery_request):
    send_orders = cdek_client.create_orders(delivery_request)

    assert send_orders
    assert len(send_orders) == 2
    order = send_orders["entity"]
    assert "uuid" in order

    order_uuid = order["uuid"]

    next_day = datetime.datetime.today() + datetime.timedelta(days=1)

    pre_alert_element = PreAlert(planned_date=next_day, shipment_point="MSK67")
    pre_alert_element.add_order(order_uuid=order_uuid)
    pre_alerts = cdek_client.create_prealerts(pre_alert_element)

    assert pre_alerts
    assert len(pre_alerts) == 2
    assert "entity" in pre_alerts
    assert "requests" in pre_alerts
    state = pre_alerts["requests"][0]["state"]
    assert state == "ACCEPTED"
