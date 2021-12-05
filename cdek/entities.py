# -*- coding: utf-8 -*-
import json
from abc import abstractmethod, ABC
from decimal import Decimal
from typing import Dict, List, Optional, Union

import datetime


class AbstractElement(ABC):
    @abstractmethod
    def to_json(self) -> dict:
        raise NotImplementedError


class DeliveryRequest(AbstractElement):
    delivery_request_element = {}

    # def __init__(self, number: str):
    #     self.number = number

    def add_order(self,
                  tariff_code: int,
                  recipient: List[dict],
                  # packages: List[dict],
                  type: int = 1,
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
                  print: Optional[str] = None
                  ) -> List:
        self.delivery_request_element['tariff_code'] = tariff_code
        self.delivery_request_element['recipient'] = recipient
        # packages: List[dict],
        self.delivery_request_element['type'] = type
        self.delivery_request_element['number'] = number
        self.delivery_request_element['comment'] = comment
        self.delivery_request_element['developer_key'] = developer_key
        self.delivery_request_element['shipment_point'] = shipment_point
        self.delivery_request_element['delivery_point'] = delivery_point
        self.delivery_request_element['date_invoice'] = date_invoice
        self.delivery_request_element['shipper_name'] = shipper_name
        self.delivery_request_element['shipper_address'] = shipper_address
        self.delivery_request_element['delivery_recipient_cost'] = delivery_recipient_cost
        self.delivery_request_element['delivery_recipient_cost_adv'] = delivery_recipient_cost_adv
        self.delivery_request_element['sender'] = sender
        self.delivery_request_element['seller'] = seller
        self.delivery_request_element['print'] = print
        return self.delivery_request_element

    @staticmethod
    def add_address(
            order_element: Optional[dict],
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
            address: Optional[str] = None
    ) -> List:
        address_element = {
            'to_location': {'code': code, 'fias_guid': fias_guid, 'postal_code': postal_code, 'longitude': longitude,
                            'latitude': latitude, 'country_code': country_code, 'region': region,
                            'region_code': region_code, 'sub_region': sub_region, 'city': city, 'address': address}}
        var = order_element.update(address_element)
        return var

    @staticmethod
    def add_package(
            order_element: List,
            size_a: Optional[int] = None,
            size_b: Optional[int] = None,
            size_c: Optional[int] = None,
            number: Optional[str] = None,
            barcode: Optional[str] = None,
            weight: Optional[int] = None
    ) -> List:
        order_number = order_element['number']
        package_number = number or order_number
        barcode = barcode or order_number

        if not (size_a and size_b and size_c):
            size_a = size_b = size_c = None

        package_element = order_element

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
            url: Optional[str] = None
    ) -> List:
        item_element = package_element
        item_element['name'] = name
        return item_element

    @staticmethod
    def add_service(
            code: str,
            parameter: Optional[str] = None
    ) -> List:
        add_service_element = {
            'code': code,
            'parameter': parameter
        }

        return add_service_element

    def to_json(self) -> dict:
        return self.delivery_request_element
