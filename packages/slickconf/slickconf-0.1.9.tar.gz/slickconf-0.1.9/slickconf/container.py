from collections.abc import Mapping, Sequence

try:
    from pydantic_core import core_schema

except ImportError:
    pass


class AnyConfig(dict):
    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if isinstance(value, dict):
                value = AnyConfig(**value)
            self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute '{item}'"
            ) from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError as e:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute '{item}'"
            ) from e


def unfold_field(x):
    if isinstance(x, Sequence) and not isinstance(x, str):
        return [unfold_field(i) for i in x]

    if isinstance(x, Mapping):
        res = {}

        for k, v in x.items():
            res[k] = unfold_field(v)

        return res

    return x


class Field(dict):
    @classmethod
    def __get_pydantic_core_schema__(self, cls, source_type):
        return core_schema.no_info_after_validator_function(
            cls.validate, core_schema.dict_schema()
        )

    @classmethod
    def validate(cls, v):
        instance = cls._recursive_init_(**v)

        return instance

    @classmethod
    def _recursive_init_(cls, **kwargs):
        node = cls()

        for key, value in kwargs.items():
            if isinstance(value, Mapping):
                value = cls._recursive_init_(**value)

            node[key] = value

        return node

    def __getitem__(self, item):
        if isinstance(item, int):
            return self["__args"][item]

        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self["__args"][key] = value
        else:
            super().__setitem__(key, value)

    def __getattr__(self, item):
        try:
            return self[item]

        except KeyError as e:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute '{item}'"
            ) from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError as e:
            raise AttributeError(
                f"{self.__class__.__name__} object has no attribute '{item}'"
            ) from e

    def __repr__(self):
        return f"{self.__class__.__name__}({dict.__repr__(self)})"

    def to_dict(self):
        return unfold_field(self)


field = Field
