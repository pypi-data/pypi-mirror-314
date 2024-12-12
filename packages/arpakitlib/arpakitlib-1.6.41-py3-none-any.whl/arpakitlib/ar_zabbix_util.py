# arpakit
import asyncio
import logging
import time
from datetime import timedelta, datetime
from typing import Any, Optional, Self

from pyzabbix import ZabbixAPI

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class ZabbixApiClient:

    def __init__(
            self,
            *,
            api_url: str,
            api_user: str,
            api_password: str,
            timeout: float = timedelta(seconds=15).total_seconds()
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        raise_for_type(api_url, str)
        self.api_url = api_url

        raise_for_type(api_user, str)
        self.api_user = api_user

        raise_for_type(api_password, str)
        self.api_password = api_password

        self.zabbix_api = ZabbixAPI(server=self.api_url, timeout=timeout)

    def login(self) -> Self:
        self.zabbix_api.login(user=self.api_user, password=self.api_password)
        return self

    def is_login_good(self) -> bool:
        try:
            self.login()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def get_host_ids(self) -> list[str]:
        kwargs = {"output": ["hostid"]}
        host_ids = self.zabbix_api.host.get(**kwargs)
        kwargs["sortfield"] = "hostid"
        kwargs["sortorder"] = "DESC"
        return [host_id["hostid"] for host_id in host_ids]

    def get_hosts(self, *, host_ids: Optional[list[str]] = None) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend",
            "selectInterfaces": "extend",
            "selectInventory": "extend",
            "selectMacros": "extend",
            "selectGroups": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        kwargs["sortfield"] = "hostid"
        kwargs["sortorder"] = "DESC"

        hosts = self.zabbix_api.host.get(**kwargs)

        return hosts

    def get_item_ids(
            self,
            *,
            host_ids: Optional[list[str]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None,
            limit: Optional[int] = None
    ) -> list[str]:
        kwargs = {"output": ["itemid"]}
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if keys is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "key_" not in kwargs["filter"].keys():
                kwargs["filter"]["key_"] = []
            kwargs["filter"]["key_"] = keys
        if names is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "name" not in kwargs["filter"].keys():
                kwargs["filter"]["name"] = []
            kwargs["filter"]["name"] = names
        if limit is not None:
            kwargs["limit"] = limit
        kwargs["sortfield"] = "itemid"
        kwargs["sortorder"] = "DESC"
        itemid_ids = self.zabbix_api.item.get(**kwargs)
        res = [host_id["itemid"] for host_id in itemid_ids]
        return res

    def get_items(
            self,
            *,
            host_ids: Optional[list[str]] = None,
            item_ids: Optional[list[str]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None,
            limit: Optional[int] = None
    ) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend",
            "selectInterfaces": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if item_ids is not None:
            kwargs["itemids"] = item_ids
        if keys is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "key_" not in kwargs["filter"].keys():
                kwargs["filter"]["key_"] = []
            kwargs["filter"]["key_"] = keys
        if names is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "name" not in kwargs["filter"].keys():
                kwargs["filter"]["name"] = []
            kwargs["filter"]["name"] = names
        if limit is not None:
            kwargs["limit"] = limit
        kwargs["sortfield"] = "itemid"
        kwargs["sortorder"] = "DESC"
        res = self.zabbix_api.item.get(**kwargs)
        return res

    def get_histories(
            self,
            *,
            host_ids: Optional[list[str]] = None,
            item_ids: Optional[list[str]] = None,
            limit: Optional[int] = None,
            history: int = 0,
            time_from: Optional[datetime] = None,
            time_till: Optional[datetime] = None
    ) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if item_ids is not None:
            kwargs["itemids"] = item_ids
        if limit is not None:
            kwargs["limit"] = limit
        if history is not None:
            kwargs["history"] = history
        if time_from is not None:
            kwargs["time_from"] = int(time.mktime((
                time_from.year, time_from.month, time_from.day, time_from.hour, time_from.minute, time_from.second, 0,
                0, 0
            )))
        if time_till is not None:
            kwargs["time_till"] = int(time.mktime((
                time_till.year, time_till.month, time_till.day, time_till.hour, time_till.minute, time_till.second, 0,
                0, 0
            )))

        histories: list[dict[str, Any]] = self.zabbix_api.history.get(**kwargs)
        for history in histories:
            if "clock" in history.keys():
                clock_ns_as_datetime = datetime.fromtimestamp(int(history["clock"]))
                if "ns" in history.keys():
                    clock_ns_as_datetime += timedelta(microseconds=int(history["ns"]) / 1000)
                    history["dt"] = clock_ns_as_datetime
                    history["assembled_key"] = (
                        f"{history["clock"]}_{history["ns"]}_{history["value"]}_{history["itemid"]}"
                    )

        return histories


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
