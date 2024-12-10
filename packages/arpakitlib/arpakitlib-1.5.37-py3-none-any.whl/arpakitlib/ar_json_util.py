# arpakit

import json
from typing import Union, Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def safely_transfer_to_json_obj(data: str) -> Union[dict, list]:
    if not isinstance(data, str):
        raise ValueError("not isinstance(data, str)")
    return json.loads(data)


def safely_transfer_to_json_str(data: Union[dict[str, Any], list[Any]]) -> str:
    if not isinstance(data, dict) and not isinstance(data, list):
        raise ValueError("not isinstance(data, dict) and not isinstance(data, list)")
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def safely_transfer_to_json_str_to_json_obj(data: Union[dict[str, Any], list[Any]]) -> Union[dict, list]:
    return safely_transfer_to_json_obj(safely_transfer_to_json_str(data))


def __example():
    pass


if __name__ == '__main__':
    __example()
