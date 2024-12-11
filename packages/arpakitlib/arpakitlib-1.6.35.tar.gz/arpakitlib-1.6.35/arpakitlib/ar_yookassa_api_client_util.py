# arpakit

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import timedelta
from typing import Optional, Any

import aiohttp
import requests

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_http_request_util import sync_make_http_request, async_make_http_request
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

"""
https://yookassa.ru/developers/api
"""


class YookassaPaymentStatuses(Enumeration):
    pending = "pending"
    waiting_for_capture = "waiting_for_capture"
    succeeded = "succeeded"
    canceled = "canceled"


class YookassaAPIException(Exception):
    pass


class YookassaAPIClient:
    def __init__(self, *, secret_key: str, shop_id: int):
        super().__init__()
        self.secret_key = secret_key
        self.shop_id = shop_id
        self.headers = {"Content-Type": "application/json"}
        self._logger = logging.getLogger(self.__class__.__name__)

    def _sync_make_request(
            self,
            *,
            method: str,
            url: str,
            **kwargs
    ) -> requests.Response:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = combine_dicts(self.headers, kwargs["headers"])
        kwargs["auth"] = (self.shop_id, self.secret_key)
        kwargs["timeout_"] = timedelta(seconds=3)
        return sync_make_http_request(
            method=method,
            url=url,
            **kwargs
        )

    def sync_create_payment(
            self,
            json_body: dict[str, Any],
            idempotence_key: Optional[str] = None
    ) -> dict[str, Any]:

        """
        json_body example
        json_body = {
            "amount": {
                "value": "2.0",
                "currency": "RUB"
            },
            "description": "description",
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/{get_tg_bot_username()}",
                "locale": "ru_RU"
            },
            "capture": True,
            "metadata": {},
            "merchant_customer_id": ""
        }
        """

        if idempotence_key is None:
            idempotence_key = str(uuid.uuid4())

        response = self._sync_make_request(
            method="POST",
            url="https://api.yookassa.ru/v3/payments",
            headers={"Idempotence-Key": idempotence_key},
            json=json_body,
        )

        json_data = response.json()

        response.raise_for_status()

        return json_data

    def sync_get_payment(self, payment_id: str) -> Optional[dict[str, Any]]:
        raise_for_type(payment_id, str)

        response = self._sync_make_request(
            method="GET",
            url=f"https://api.yookassa.ru/v3/payments/{payment_id}",
            headers=self.headers
        )

        json_data = response.json()

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return json_data

    async def async_make_request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = combine_dicts(self.headers, kwargs["headers"])
        kwargs["auth"] = aiohttp.BasicAuth(login=str(self.shop_id), password=self.secret_key)
        kwargs["timeout_"] = timedelta(seconds=3)
        return await async_make_http_request(
            method=method,
            url=url,
            **kwargs
        )

    async def async_create_payment(
            self, json_body: dict[str, Any], idempotence_key: Optional[str] = None
    ) -> dict[str, Any]:

        """
        json_body example
        json_body = {
            "amount": {
                "value": "2.0",
                "currency": "RUB"
            },
            "description": "description",
            "confirmation": {
                "type": "redirect",
                "return_url": f"https://t.me/{get_tg_bot_username()}",
                "locale": "ru_RU"
            },
            "capture": True,
            "metadata": {},
            "merchant_customer_id": ""
        }
        """

        if idempotence_key is None:
            idempotence_key = str(uuid.uuid4())

        response = await self.async_make_request(
            method="POST",
            url="https://api.yookassa.ru/v3/payments",
            headers={"Idempotence-Key": idempotence_key},
            json=json_body,
        )

        json_data = await response.json()

        response.raise_for_status()

        return json_data

    async def async_get_payment(self, payment_id: str) -> Optional[dict[str, Any]]:
        raise_for_type(payment_id, str)

        response = await self.async_make_request(
            method="GET",
            url=f"https://api.yookassa.ru/v3/payments/{payment_id}",
        )

        json_data = await response.json()

        if response.status == 404:
            return None

        response.raise_for_status()

        return json_data


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
