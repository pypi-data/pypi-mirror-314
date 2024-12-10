# arpakit

import asyncio
import logging
from abc import ABC
from typing import Optional, Any, Union, Callable, Iterable

from aiogram import types, BaseMiddleware, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ChatType, ParseMode
from aiogram.exceptions import AiogramError
from aiogram.filters import CommandObject, Filter
from aiogram.filters.callback_data import CallbackData
from pydantic import BaseModel

from arpakitlib.ar_need_type_util import parse_need_type, NeedTypes
from arpakitlib.ar_parse_command import BadCommandFormat, parse_command
from arpakitlib.ar_type_util import raise_for_types, raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

_logger = logging.getLogger(__name__)


class TextFilter(Filter):

    def __init__(
            self,
            *texts: Union[str, Iterable[str]],
            ignore_case: bool = True
    ) -> None:
        self.ignore_case = ignore_case
        self.texts = set()

        for text in texts:

            if isinstance(text, str):
                if ignore_case is True:
                    text = text.lower()
                text = text.strip()
                self.texts.add(text)

            elif isinstance(text, Iterable):
                for text_ in text:
                    raise_for_type(text_, str)
                    if ignore_case is True:
                        text_ = text_.lower()
                    text_ = text_.strip()
                    self.texts.add(text_)

            else:
                raise TypeError(f"text has bad type = {type(text)}")

    async def __call__(self, message: types.Message, *args, **kwargs) -> bool:
        raise_for_type(message, types.Message)

        if message.text is None:
            return False

        text = message.text.strip()
        if self.ignore_case is True:
            text = text.lower()

        return text in self.texts


class IsPrivateChat(Filter):
    async def __call__(self, update: types.Message | types.CallbackQuery) -> bool:
        if isinstance(update, types.Message):
            return update.chat.type == ChatType.PRIVATE
        elif isinstance(update, types.CallbackQuery):
            return update.message.chat.type == ChatType.PRIVATE
        else:
            return False


_used_cd_prefixes = set()


def get_used_cd_prefixes() -> set[str]:
    return _used_cd_prefixes


def generate_cd_prefix(string: str) -> str:
    res = 0
    for s_ in string:
        res += ord(s_)
    res += len(string)
    res = str(res)
    return res


class BaseCD(CallbackData, prefix="BaseCD"):

    def __init_subclass__(cls, **kwargs):
        if not cls.__name__.endswith("CD"):
            raise ValueError("callback data class should ends with CD")

        if "prefix" not in kwargs:
            kwargs["prefix"] = str(generate_cd_prefix(cls.__name__.lower().removesuffix("cd")))
        prefix = kwargs["prefix"]

        if prefix in _used_cd_prefixes:
            raise ValueError(f"prefix({prefix}) already in _used_cd_prefixes({_used_cd_prefixes})")
        _used_cd_prefixes.add(prefix)

        super().__init_subclass__(**kwargs)


class WithFromCD(BaseCD, prefix="WithFromCD"):
    from_: Optional[str] = None


class BadTgCommandFormat(BadCommandFormat):
    pass


class BaseTgCommandParam(BaseModel):
    key: str


class TgCommandFlagParam(BaseTgCommandParam):
    pass


class TgCommandKeyValueParam(BaseTgCommandParam):
    need_type: str
    index: Optional[int] = None
    required: bool = False
    default: Optional[Any] = None

    @property
    def has_index(self) -> bool:
        return False if self.index is None else True


def as_tg_command(
        *params: TgCommandFlagParam | TgCommandKeyValueParam,
        desc: str | None = None,
        check_passwd: Callable | str | None = None,
        passwd: str | None = None,
        remove_message_after_correct_passwd: bool = True
):
    _PASSWD_KEY = "passwd"
    _HELP_FLAG = "help"

    params = list(params)

    if check_passwd is None and passwd is not None:
        check_passwd = passwd
    if check_passwd is not None:
        raise_for_types(check_passwd, [Callable, str])
        params.append(TgCommandKeyValueParam(key=_PASSWD_KEY, required=True, index=None, need_type=NeedTypes.str_))

    params.append(TgCommandFlagParam(key=_HELP_FLAG))

    _were_keys = set()
    for param in params:
        if param.key in _were_keys:
            raise ValueError(f"key={param.key} is duplicated")
        _were_keys.add(param.key)
    _were_keys.clear()

    _were_indexes = set()
    for param in params:
        if not isinstance(param, TgCommandKeyValueParam) or not param.has_index:
            continue
        if param.index in _were_indexes:
            raise ValueError(f"index={param.index} is duplicated")
        _were_indexes.add(param.index)

    def decorator(handler):

        async def new_handler(*args, **kwargs):
            message: types.Message = args[0]
            if not isinstance(message, types.Message):
                raise TypeError("not isinstance(message, types.Message)")

            command: CommandObject = kwargs["command"]

            try:
                parsed_command = parse_command(command.text)
                kwargs["parsed_command"] = parsed_command

                if (
                        not parsed_command.values_without_key
                        and len(parsed_command.flags) == 1
                        and parsed_command.has_flag(_HELP_FLAG)
                ):
                    text = f"<b>Command</b> /{command.command}"
                    if desc is not None:
                        text += "\n\n" + desc
                    text += "\n\n"

                    if check_passwd is not None:
                        text += "Passwd is required\n\n"

                    text += "<b>Keys:</b>\n"
                    tg_command_key_value_params = list(filter(lambda p: isinstance(p, TgCommandKeyValueParam), params))
                    if tg_command_key_value_params:
                        for i, _param in enumerate(tg_command_key_value_params):
                            text += f"{i + 1}. <code>{_param.key}</code>"
                            if _param.has_index:
                                text += f", {_param.index}"
                            text += f", {_param.need_type}"
                            if _param.required is True:
                                text += ", <b>required</b>"
                            else:
                                text += ", not required"
                            if _param.default is not None:
                                text += f", <code>{_param.default}</code>"
                            text = text.strip()
                            text += "\n"
                    else:
                        text += "<i>No keys</i>"
                    text = text.strip()
                    text += "\n\n"

                    text += "<b>Flags:</b>\n"
                    tg_command_flag_params = list(filter(lambda p: isinstance(p, TgCommandFlagParam), params))
                    if tg_command_flag_params:
                        for i, _param in enumerate(tg_command_flag_params):
                            text += f"{i + 1}. <code>-{_param.key}</code>\n"
                    else:
                        text += "<i>No flags</i>"
                    text = text.strip()
                    text += "\n\n"

                    text += f"<code>/{command.command} -{_HELP_FLAG}</code>"
                    text += f"\n<code>/{command.command}</code>"

                    await message.answer(text=text.strip())
                    return

                if check_passwd is not None:
                    passwd_ = parsed_command.get_value_by_key(_PASSWD_KEY)
                    if not passwd_:
                        is_passwd_correct = False
                    elif isinstance(check_passwd, Callable):
                        is_passwd_correct = check_passwd(
                            passwd=passwd_, message=message, parsed_command=parsed_command
                        )
                    elif isinstance(check_passwd, str):
                        is_passwd_correct = (check_passwd == passwd_)
                    else:
                        raise TypeError("check_passwd is not not Callable and not str")
                    if not is_passwd_correct:
                        await message.answer("Passwd is incorrect")
                        return
                    if remove_message_after_correct_passwd:
                        try:
                            await message.delete()
                        except AiogramError as e:
                            _logger.error(e)
                    try:
                        await message.answer("Passwd is ok")
                    except AiogramError as e:
                        _logger.error(e)

                for _param in params:
                    if isinstance(_param, TgCommandFlagParam):
                        kwargs[_param.key] = parsed_command.has_flag(_param.key)

                    elif isinstance(_param, TgCommandKeyValueParam):
                        if _param.key in kwargs.keys():
                            raise BadTgCommandFormat(f"{_param.key} already in {kwargs.keys()}")

                        value_by_key: Optional[str] = parsed_command.get_value_by_key(_param.key)

                        value_by_index: Optional[str] = None
                        if _param.has_index:
                            value_by_index = parsed_command.get_value_by_index(_param.index)

                        if value_by_key is not None and value_by_index is not None:
                            raise BadTgCommandFormat(
                                f"Value was found by key={_param.key} and index={_param.index}"
                            )

                        value = value_by_key if value_by_key is not None else value_by_index

                        if value is None:
                            if _param.default is not None:
                                value = _param.default
                            elif _param.required is True:
                                raise BadTgCommandFormat(
                                    f"Value (key={_param.key}, index={_param.index}) is required"
                                )
                        else:
                            value = parse_need_type(value=value, need_type=_param.need_type)

                        kwargs[_param.key] = value

                    else:
                        raise TypeError(f"bad type for param, {type(_param)}")

            except BadCommandFormat as e:
                await message.answer(
                    f"<b>Bad command usage</b> /{command.command}\n\n"

                    "<b>Error</b>\n"
                    f"{e}\n\n"

                    f"Use <code>/{command.command} -{_HELP_FLAG}</code> for getting help info"
                )
                return

            return await handler(*args, **kwargs)

        return new_handler

    return decorator


class SimpleMiddleware(BaseMiddleware, ABC):
    def __init__(self):
        self.middleware_name = self.__class__.__name__
        self._logger = logging.getLogger(self.__class__.__name__)


def create_tg_bot(*, tg_bot_token: str, tg_bot_proxy_url: str | None = None) -> Bot:
    session: AiohttpSession | None = None
    if tg_bot_proxy_url:
        session = AiohttpSession(proxy=tg_bot_proxy_url)
    tg_bot = Bot(
        token=tg_bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            disable_notification=False,
            link_preview_is_disabled=True
        ),
        session=session
    )
    return tg_bot


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
