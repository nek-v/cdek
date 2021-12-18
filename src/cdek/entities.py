# -*- coding: utf-8 -*-
import datetime
import decimal
import json
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional, Union

Date = Union[datetime.datetime, datetime.date]


class AbstractElement(ABC):
    @abstractmethod
    def to_json(self) -> json:
        raise NotImplementedError


class DeliveryRequest(AbstractElement):
    delivery_request_element = {}

    def add_order(
        self,
        tariff_code: int,
        recipient: List[dict],
        order_type: int = 1,
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
        sender: List[dict] = None,
        seller: Optional[List[dict]] = None,
        print_order: Optional[str] = None,
    ) -> List:
        self.delivery_request_element["tariff_code"] = tariff_code
        self.delivery_request_element["recipient"] = recipient
        self.delivery_request_element["type"] = order_type
        self.delivery_request_element["number"] = number
        self.delivery_request_element["comment"] = comment
        self.delivery_request_element["developer_key"] = developer_key
        self.delivery_request_element["shipment_point"] = shipment_point
        self.delivery_request_element["delivery_point"] = delivery_point
        self.delivery_request_element["date_invoice"] = date_invoice
        self.delivery_request_element["shipper_name"] = shipper_name
        self.delivery_request_element["shipper_address"] = shipper_address
        self.delivery_request_element[
            "delivery_recipient_cost"
        ] = delivery_recipient_cost
        self.delivery_request_element[
            "delivery_recipient_cost_adv"
        ] = delivery_recipient_cost_adv
        self.delivery_request_element["sender"] = sender
        self.delivery_request_element["seller"] = seller
        self.delivery_request_element["print"] = print_order
        return self.delivery_request_element

    @staticmethod
    def add_address(
        order_element: dict,
        location_type: str,
        code: Optional[str] = None,
        fias_guid: Optional[str] = None,
        postal_code: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        country_code: Optional[str] = None,
        region: Optional[str] = None,
        region_code: Optional[int] = None,
        sub_region: Optional[str] = None,
        city: Optional[str] = None,
        address: Optional[str] = None,
    ) -> List:
        if location_type == "from_location" or location_type == "to_location":
            address_element = {
                location_type: {
                    "code": code,
                    "fias_guid": fias_guid,
                    "postal_code": postal_code,
                    "longitude": longitude,
                    "latitude": latitude,
                    "country_code": country_code,
                    "region": region,
                    "region_code": region_code,
                    "sub_region": sub_region,
                    "city": city,
                    "address": address,
                }
            }
            order_element.update(address_element)
        else:
            raise ValueError(
                "Invalid location_type value. The value can be 'from_location' or 'to_location'."
            )
        return order_element

    @staticmethod
    def add_package(
        order_element: dict,
        number: str,
        weight: int,
        length: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        comment: Optional[str] = "Package",
    ) -> List:
        if not (length and width and height):
            length = width = height = None

        package_element = {
            "packages": [
                {
                    "number": number,
                    "weight": weight,
                    "length": length,
                    "width": width,
                    "height": height,
                    "comment": comment,
                }
            ]
        }
        order_element.update(package_element)
        return package_element

    @staticmethod
    def add_item(
        package_element: dict,
        name: str,
        ware_key: str,
        cost: Union[Decimal, float],
        weight: int,
        amount: int,
        marking: Optional[str] = None,
        payment: Union[Decimal, float] = 0,
        weight_gross: Optional[int] = None,
        name_i18n: Optional[str] = None,
        brand: Optional[str] = None,
        country_code: Optional[str] = None,
        material: Optional[int] = None,
        wifi_gsm: Optional[bool] = None,
        url: Optional[str] = None,
    ) -> List:
        item_element = {
            "name": name,
            "ware_key": ware_key,
            "cost": cost,
            "weight": weight,
            "amount": amount,
            "marking": marking,
            "payment": {"value": payment},
            "weight_gross": weight_gross,
            "name_i18n": name_i18n,
            "brand": brand,
            "country_code": country_code,
            "material": material,
            "wifi_gsm": wifi_gsm,
            "url": url,
        }
        for p in package_element["packages"]:
            p["items"] = [item_element]
        return package_element

    @staticmethod
    def add_service(
        order_element: dict, code: str, parameter: Optional[str] = None
    ) -> List:
        service_element = {
            "services": [{"code": code, "parameter": parameter}]
        }
        order_element.update(service_element)
        return service_element

    def to_json(self) -> json:
        return json.dumps(self.delivery_request_element, cls=DecimalEncoder)


class PreAlert(AbstractElement):
    pre_alert_element = {}

    def __init__(self, planned_date: Date, shipment_point: str):
        self.pre_alert_element = {
            "orders": [],
            "planned_date": planned_date.astimezone().strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            ),
            "shipment_point": shipment_point,
        }

    def add_order(
        self,
        order_uuid: Optional[str] = None,
        cdek_number: Optional[int] = None,
        im_number: Optional[int] = None,
    ) -> List:
        order_element = {
            "order_uuid": order_uuid,
            "cdek_number": cdek_number,
            "im_number": im_number,
        }
        self.pre_alert_element["orders"] = order_element
        return self.pre_alert_element

    def to_json(self) -> json:
        return json.dumps(self.pre_alert_element, cls=DecimalEncoder)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
