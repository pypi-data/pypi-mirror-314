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
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep
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

    def _sync_make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        max_tries = 7
        tries = 0

        kwargs["url"] = url
        kwargs["method"] = method
        kwargs["timeout"] = (timedelta(seconds=3).total_seconds(), timedelta(seconds=3).total_seconds())
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = combine_dicts(self.headers, kwargs["headers"])
        kwargs["auth"] = (self.shop_id, self.secret_key)

        while True:
            self._logger.info(f"{method} {url}")
            tries += 1
            try:
                return requests.request(**kwargs)
            except Exception as err:
                self._logger.warning(f"{tries}/{max_tries} {err} {method} {url}")
                if tries >= max_tries:
                    raise YookassaAPIException(err)
                sync_safe_sleep(timedelta(seconds=0.1).total_seconds())
                continue

    async def _async_make_request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        max_tries = 7
        tries = 0

        kwargs["url"] = url
        kwargs["method"] = method
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timedelta(seconds=15).total_seconds())
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"] = combine_dicts(self.headers, kwargs["headers"])
        kwargs["auth"] = aiohttp.BasicAuth(login=str(self.shop_id), password=self.secret_key)

        while True:
            self._logger.info(f"{method} {url}")
            tries += 1
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(**kwargs) as response:
                        await response.read()
                        return response
            except Exception as err:
                self._logger.warning(f"{tries}/{max_tries} {err} {method} {url}")
                if tries >= max_tries:
                    raise YookassaAPIException(err)
                await async_safe_sleep(timedelta(seconds=0.1).total_seconds())
                continue

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

        headers = combine_dicts({"Idempotence-Key": idempotence_key})

        response = self._sync_make_request(
            method="POST",
            url="https://api.yookassa.ru/v3/payments",
            headers=headers,
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

        headers = combine_dicts({"Idempotence-Key": idempotence_key})

        response = await self._async_make_request(
            method="POST",
            url="https://api.yookassa.ru/v3/payments",
            headers=headers,
            json=json_body,
        )

        json_data = await response.json()

        response.raise_for_status()

        return json_data

    async def async_get_payment(self, payment_id: str) -> Optional[dict[str, Any]]:
        raise_for_type(payment_id, str)

        response = await self._async_make_request(
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
