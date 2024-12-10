# arpakit

from typing import Union

from pydantic_settings import BaseSettings

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_env_example(settings_class: Union[BaseSettings, type[BaseSettings]]):
    res = ""
    for k in settings_class.model_fields:
        res += f"{k}=\n"
    return res


def __example():
    pass
