# arpakit

from typing import Union, Iterator, Iterable

_ARPAKIT_LIB_MODULE_VERSION = "3.0"

ValueType = Union[int, str]
ValuesForParseType = Union[ValueType, Iterable[ValueType]]


class Enumeration:
    @classmethod
    def iter_values(cls) -> Iterator[ValueType]:
        big_dict = {}
        for class_ in reversed(cls.mro()):
            big_dict.update(class_.__dict__)
        big_dict.update(cls.__dict__)

        keys = list(big_dict.keys())

        for key in keys:

            if not isinstance(key, str):
                continue

            if key.startswith("__") or key.endswith("__"):
                continue

            value = big_dict[key]
            if type(value) not in [str, int]:
                continue

            yield value

    @classmethod
    def values_set(cls) -> set[ValueType]:
        return set(cls.iter_values())

    @classmethod
    def values_list(cls) -> list[ValueType]:
        return list(cls.iter_values())

    @classmethod
    def parse_values(cls, *values: ValuesForParseType, validate: bool = False) -> list[ValueType]:
        res = []

        for value in values:

            if isinstance(value, str) or isinstance(value, int):
                if validate is True and value not in cls.values_set():
                    raise ValueError(f"validate is True and {value} not in {cls.values_set()}")
                res.append(value)

            elif isinstance(value, Iterable):
                for value_ in value:
                    if isinstance(value_, str) or isinstance(value_, int):
                        if validate is True and value_ not in cls.values_set():
                            raise ValueError(f"validate is True and {value_} not in {cls.values_set()}")
                        res.append(value_)
                    else:
                        raise TypeError(f"bad type, value={value}, type={type(value)}")

            else:
                raise TypeError(f"bad type, value={value}, type={type(value)}")

        return res

    @classmethod
    def parse_and_validate_values(cls, *values: ValuesForParseType) -> list[ValueType]:
        return cls.parse_values(*values, validate=True)


def __example():
    pass


if __name__ == '__main__':
    __example()
