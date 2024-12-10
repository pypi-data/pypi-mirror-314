# arpakit

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from datetime import timedelta, datetime, time
from typing import Any
from urllib.parse import urljoin

import aiohttp
import cachetools
from aiohttp import ClientResponse, ClientTimeout, ClientResponseError
from pydantic import ConfigDict, BaseModel

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_json_util import safely_transfer_to_json_str
from arpakitlib.ar_sleep_util import async_safe_sleep
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class Weekdays(Enumeration):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class Months(Enumeration):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    def simple_json(self) -> str:
        return safely_transfer_to_json_str(self.model_dump(mode="json"))


class GroupAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    uust_api_id: int
    title: str
    faculty: str | None
    course: int | None
    difference_level: int | None = None
    uust_api_data: dict[str, Any]

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, arpakit_uust_api_data: dict[str, Any]) -> GroupAPIModel:
        return GroupAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data}
        ))


class TeacherAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    uust_api_id: int
    name: str | None
    surname: str | None
    patronymic: str | None
    fullname: str | None
    shortname: str | None
    posts: list[str]
    post: str | None
    units: list[str]
    unit: str | None
    difference_level: int | None
    uust_api_data: dict[str, Any]

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, arpakit_uust_api_data: dict[str, Any]) -> TeacherAPIModel:
        return TeacherAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data}
        ))


class GroupLessonAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: time | None
    time_end: time | None
    numbers: list[int]
    location: str | None
    teacher_uust_api_id: int | None
    group_uust_api_id: int | None
    group: GroupAPIModel
    teacher: TeacherAPIModel | None
    uust_api_data: dict[str, Any]

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, arpakit_uust_api_data: dict[str, Any]) -> GroupLessonAPIModel:
        return GroupLessonAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data},
            {
                "group": GroupAPIModel.from_arpakit_uust_api_data(
                    arpakit_uust_api_data=arpakit_uust_api_data["group"]
                )
            },
            {
                "teacher": (
                    TeacherAPIModel.from_arpakit_uust_api_data(
                        arpakit_uust_api_data=arpakit_uust_api_data["teacher"]
                    )
                    if arpakit_uust_api_data["teacher"] is not None
                    else None
                )
            },
        ))

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class TeacherLessonAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: time | None
    time_end: time | None
    numbers: list[int]
    location: str | None
    group_uust_api_ids: list[int]
    teacher_uust_api_id: int
    teacher: TeacherAPIModel
    groups: list[GroupAPIModel]
    uust_api_data: dict[str, Any]

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, arpakit_uust_api_data: dict[str, Any]) -> TeacherLessonAPIModel:
        return TeacherLessonAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data},
            {
                "teacher": TeacherAPIModel.from_arpakit_uust_api_data(
                    arpakit_uust_api_data=arpakit_uust_api_data["teacher"]
                )
            },
            {
                "groups": [
                    GroupAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d)
                    for d in arpakit_uust_api_data["groups"]
                ]
            },
        ))

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class CurrentSemesterAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    value: str
    raw_value: str

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, *, arpakit_uust_api_data: dict[str, Any]) -> CurrentSemesterAPIModel:
        return CurrentSemesterAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data}
        ))


class CurrentWeekAPIModel(BaseAPIModel):
    id: int
    creation_dt: datetime
    sync_from_uust_api_dt: datetime
    value: str

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, *, arpakit_uust_api_data: dict[str, Any]) -> CurrentWeekAPIModel:
        return CurrentWeekAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data}
        ))


class WeatherInUfaAPIModel(BaseAPIModel):
    temperature: float
    temperature_feels_like: float
    description: str
    wind_speed: float
    sunrise_dt: datetime
    sunset_dt: datetime
    has_rain: bool
    has_snow: bool
    data: dict

    arpakit_uust_api_data: dict[str, Any]

    @classmethod
    def from_arpakit_uust_api_data(cls, arpakit_uust_api_data: dict[float, Any]) -> WeatherInUfaAPIModel:
        return WeatherInUfaAPIModel.model_validate(combine_dicts(
            arpakit_uust_api_data,
            {"arpakit_uust_api_data": arpakit_uust_api_data}
        ))


class ARPAKITScheduleUUSTAPIClient:
    def __init__(
            self,
            *,
            base_url: str = "https://api.schedule-uust.arpakit.com/api/v1",
            api_key: str | None = "viewer",
            use_cache: bool = False,
            cache_ttl: int | float | None = timedelta(minutes=10).total_seconds()
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
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        if cache_ttl is not None:
            self.ttl_cache = cachetools.TTLCache(maxsize=100, ttl=cache_ttl)
        else:
            self.ttl_cache = None

    def clear_a_s_u_api_client(self):
        if self.ttl_cache is not None:
            self.ttl_cache.clear()

    async def _async_make_request(self, *, method: str = "GET", url: str, **kwargs) -> ClientResponse:
        max_tries = 7
        tries = 0

        kwargs["url"] = url
        kwargs["method"] = method
        kwargs["timeout"] = ClientTimeout(total=timedelta(seconds=15).total_seconds())
        kwargs["headers"] = self.headers

        cache_key = (
            "_async_make_request",
            hashlib.sha256(json.dumps(kwargs, ensure_ascii=False, default=str).encode()).hexdigest()
        )

        if self.use_cache and self.ttl_cache is not None:
            if cache_key in self.ttl_cache:
                return self.ttl_cache[cache_key]

        while True:
            tries += 1
            self._logger.info(f"{method} {url}")
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(**kwargs) as response:
                        await response.read()
                        if self.use_cache and self.ttl_cache is not None:
                            self.ttl_cache[cache_key] = response
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

    async def get_required_current_week_value(self) -> int:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "get_current_week"))
        response.raise_for_status()
        json_data = await response.json()
        raise_for_type(json_data["value"], int)
        return json_data["value"]

    async def get_current_semester(self) -> CurrentSemesterAPIModel | None:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "get_current_semester"))
        json_data = await response.json()
        if json_data is None:
            return None
        if "error_code" in json_data and json_data["error_code"] == "CURRENT_SEMESTER_NOT_FOUND":
            return None
        response.raise_for_status()
        return CurrentSemesterAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=json_data)

    async def get_current_week(self) -> CurrentWeekAPIModel | None:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "get_current_week"))
        json_data = await response.json()
        if json_data is None:
            return None
        if "error_code" in json_data and json_data["error_code"] == "CURRENT_WEEK_NOT_FOUND":
            return None
        response.raise_for_status()
        return CurrentWeekAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=json_data)

    async def get_log_file_content(self) -> str | None:

        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "extra/get_log_file"))
        response.raise_for_status()
        text_data = await response.text()
        return text_data

    async def get_groups(self) -> list[GroupAPIModel]:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "group/get_groups"))
        response.raise_for_status()
        json_data = await response.json()
        return [GroupAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_group(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> GroupAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "group/get_group"),
            params=params
        )
        json_data = await response.json()
        if "error_code" in json_data and json_data["error_code"] == "GROUP_NOT_FOUND":
            return None
        response.raise_for_status()
        return GroupAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=json_data)

    async def find_groups(
            self, *, q: str
    ) -> list[GroupAPIModel]:
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "group/find_groups"),
            params={"q": q.strip()}
        )
        response.raise_for_status()
        json_data = await response.json()
        return [GroupAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_teachers(self) -> list[TeacherAPIModel]:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "teacher/get_teachers"))
        response.raise_for_status()
        json_data = await response.json()
        return [TeacherAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_teacher(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> TeacherAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "teacher/get_teacher"),
            params=params
        )
        json_data = await response.json()
        if "error_code" in json_data and json_data["error_code"] == "TEACHER_NOT_FOUND":
            return None
        response.raise_for_status()
        return TeacherAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=json_data)

    async def find_teachers(
            self, *, q: str
    ) -> list[TeacherAPIModel]:
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "teacher/find_teachers"),
            params={"q": q.strip()}
        )
        response.raise_for_status()
        json_data = await response.json()
        return [TeacherAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_group_lessons(
            self,
            *,
            filter_group_id: int | None = None,
            filter_group_uust_api_id: int | None = None
    ) -> list[GroupLessonAPIModel]:
        params = {}
        if filter_group_id is not None:
            params["filter_group_id"] = filter_group_id
        if filter_group_uust_api_id is not None:
            params["filter_group_uust_api_id"] = filter_group_uust_api_id
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "group_lesson/get_group_lessons"),
            params=params
        )
        response.raise_for_status()
        json_data = await response.json()
        return [GroupLessonAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_teacher_lessons(
            self,
            *,
            filter_teacher_id: int | None = None,
            filter_teacher_uust_api_id: int | None = None
    ) -> list[TeacherLessonAPIModel]:
        params = {}
        if filter_teacher_id is not None:
            params["filter_teacher_id"] = filter_teacher_id
        if filter_teacher_uust_api_id is not None:
            params["filter_teacher_uust_api_id"] = filter_teacher_uust_api_id
        response = await self._async_make_request(
            method="GET",
            url=urljoin(self.base_url, "teacher_lesson/get_teacher_lessons"),
            params=params
        )
        response.raise_for_status()
        json_data = await response.json()
        return [TeacherLessonAPIModel.from_arpakit_uust_api_data(arpakit_uust_api_data=d) for d in json_data]

    async def get_weather_in_ufa(self) -> WeatherInUfaAPIModel:
        response = await self._async_make_request(method="GET", url=urljoin(self.base_url, "get_weather_in_ufa"))
        response.raise_for_status()
        json_data = await response.json()
        return WeatherInUfaAPIModel.from_arpakit_uust_api_data(json_data)


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
