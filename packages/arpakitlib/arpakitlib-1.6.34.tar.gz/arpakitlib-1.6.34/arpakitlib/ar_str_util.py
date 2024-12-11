# arpakit

from typing import Optional

from bs4 import BeautifulSoup

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def str_in(string: str, main_string: str, *, max_diff: Optional[int] = None) -> bool:
    if string not in main_string:
        return False

    if max_diff is None:
        return True

    diff = len(main_string) - len(string)
    if diff <= max_diff:
        return True

    return False


def bidirectional_str_in(string1: str, string2: str, *, max_diff: Optional[int] = None) -> bool:
    if (
            str_in(string=string1, main_string=string2, max_diff=max_diff)
            or str_in(string=string2, main_string=string1, max_diff=max_diff)
    ):
        return True
    return False


def str_startswith(string: str, main_string: str, max_diff: Optional[int] = None) -> bool:
    if not main_string.startswith(string):
        return False

    if max_diff is None:
        return True

    diff = len(main_string) - len(string)
    if diff <= max_diff:
        return True

    return False


def bidirectional_str_startswith(string1: str, string2: str, max_diff: Optional[int] = None) -> bool:
    if str_startswith(string1, string2, max_diff=max_diff) or str_startswith(string2, string1, max_diff=max_diff):
        return True
    return False


def blank_if_none(string: Optional[str] = None) -> str:
    if string is None:
        return ""
    return string


def remove_html(string: str) -> str:
    raise_for_type(string, str)
    return BeautifulSoup(string, "html.parser").text


def remove_tags(string: str) -> str:
    raise_for_type(string, str)
    return string.replace("<", "").replace(">", "")


def remove_tags_and_html(string: str) -> str:
    raise_for_type(string, str)
    return remove_tags(remove_html(string))


def __example():
    pass


if __name__ == '__main__':
    __example()
