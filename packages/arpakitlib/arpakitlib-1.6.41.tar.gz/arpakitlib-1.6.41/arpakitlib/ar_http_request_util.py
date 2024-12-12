# arpakit

import asyncio
import logging
from datetime import timedelta

import aiohttp
import requests
from aiohttp_socks import ProxyConnector

from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


def sync_make_http_request(
        *,
        method: str = "GET",
        url: str,
        max_tries_: int = 9,
        proxy_url_: str | None = None,
        raise_for_status_: bool = False,
        timeout_: timedelta | float = timedelta(seconds=15).total_seconds(),
        **kwargs
) -> requests.Response:
    if isinstance(timeout_, float):
        timeout_ = timedelta(seconds=timeout_)
    raise_for_type(timeout_, timedelta)

    tries_counter = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if timeout_ is not None:
        kwargs["timeout"] = timeout_.total_seconds()
    if proxy_url_:
        kwargs["proxies"] = {
            "http": proxy_url_,
            "https": proxy_url_
        }
    if "allow_redirects" not in kwargs:
        kwargs["allow_redirects"] = True

    while True:
        tries_counter += 1
        _logger.info(f"{method} {url} {kwargs.get('params')}")
        try:
            response = requests.request(**kwargs)
            if raise_for_status_:
                response.raise_for_status()
            return response
        except BaseException as exception:
            _logger.warning(f"{tries_counter}/{max_tries_} {method} {url} {exception}")
            if tries_counter >= max_tries_:
                raise exception
            sync_safe_sleep(timedelta(seconds=0.1).total_seconds())
            continue


async def async_make_http_request(
        *,
        method: str = "GET",
        url: str,
        max_tries_: int = 9,
        proxy_url_: str | None = None,
        raise_for_status_: bool = False,
        timeout_: timedelta | None = timedelta(seconds=15),
        **kwargs
) -> aiohttp.ClientResponse:
    tries_counter = 0

    kwargs["method"] = method
    kwargs["url"] = url
    if timeout_ is not None:
        kwargs["timeout"] = aiohttp.ClientTimeout(total=timeout_.total_seconds())
    if "allow_redirects" not in kwargs:
        kwargs["allow_redirects"] = True

    proxy_connector: ProxyConnector | None = None
    if proxy_url_:
        proxy_connector = ProxyConnector.from_url(proxy_url_)

    while True:
        tries_counter += 1
        _logger.info(f"{method} {url} {kwargs.get('params')}")
        try:
            async with aiohttp.ClientSession(connector=proxy_connector) as session:
                async with session.request(**kwargs) as response:
                    if raise_for_status_:
                        response.raise_for_status()
                    await response.read()
                    return response
        except BaseException as exception:
            _logger.warning(f"{tries_counter}/{max_tries_} {method} {url} {exception}")
            if tries_counter >= max_tries_:
                raise exception
            await async_safe_sleep(timedelta(seconds=0.1).total_seconds())
            continue


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
