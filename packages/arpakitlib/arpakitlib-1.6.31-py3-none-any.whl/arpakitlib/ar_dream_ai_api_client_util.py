# arpakit

import asyncio
import logging
from datetime import timedelta
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientResponseError, ClientResponse, ClientTimeout
from pydantic import ConfigDict, BaseModel

from arpakitlib.ar_base64_util import convert_base64_string_to_bytes
from arpakitlib.ar_json_util import safely_transfer_to_json_str
from arpakitlib.ar_sleep_util import async_safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    def simple_json(self) -> str:
        return safely_transfer_to_json_str(self.model_dump(mode="json"))


class GenerateImageFromNumberResApiModel(BaseAPIModel):
    image_filename: str
    image_url: str
    image_base64: str

    def save_file(self, filepath: str):
        with open(filepath, mode="wb") as f:
            f.write(convert_base64_string_to_bytes(base64_string=self.image_base64))
        return filepath


class DreamAIAPIClient:
    def __init__(
            self,
            *,
            base_url: str = "https://api.dream_ai.arpakit.com/api/v1",
            api_key: str | None = None
    ):
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        base_url = base_url.strip()
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key is not None:
            self.headers.update({"apikey": api_key})

    async def _async_make_request(self, *, method: str = "GET", url: str, **kwargs) -> ClientResponse:
        max_tries = 7
        tries = 0

        kwargs["url"] = url
        kwargs["method"] = method
        kwargs["timeout"] = ClientTimeout(total=timedelta(seconds=15).total_seconds())
        kwargs["headers"] = self.headers

        while True:
            tries += 1
            self._logger.info(f"{method} {url}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(**kwargs) as response:
                        await response.read()
                        return response
            except Exception as err:
                self._logger.warning(f"{tries}/{max_tries} {err} {method} {url}")
                if tries >= max_tries:
                    raise err
                await async_safe_sleep(timedelta(seconds=0.1).total_seconds())
                continue

    async def healthcheck(self) -> bool:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "healthcheck"))
        response.raise_for_status()
        json_data = await response.json()
        return json_data["data"]["healthcheck"]

    async def is_healthcheck_good(self) -> bool:
        try:
            return await self.healthcheck()
        except ClientResponseError:
            return False

    async def auth_healthcheck(self) -> bool:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "auth_healthcheck"))
        response.raise_for_status()
        json_data = await response.json()
        return json_data["data"]["auth_healthcheck"]

    async def is_auth_healthcheck_good(self) -> bool:
        try:
            return await self.auth_healthcheck()
        except ClientResponseError:
            return False

    async def generate_image_from_number(self, *, number: int) -> GenerateImageFromNumberResApiModel:
        response = await self._async_make_request(
            method="GET", url=urljoin(self.base_url, "generate_image_from_number"),
            params={"number": number}
        )
        response.raise_for_status()
        json_data = await response.json()
        return GenerateImageFromNumberResApiModel.model_validate(json_data)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
