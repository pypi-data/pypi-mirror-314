from enum import Enum


class DataType(Enum):
    NONE = 0
    INTEGER = 1
    FLOAT = 2
    STRING = 3
    BOOLEAN = 4
    LIST = 5
    DICTIONARY = 6

    @classmethod
    def get_type(cls, value):
        _type = cls.STRING

        if value is None:
            _type = cls.NONE
        elif isinstance(value, bool):
            _type = cls.BOOLEAN
        elif isinstance(value, int):
            _type = cls.INTEGER
        elif isinstance(value, float):
            _type = cls.FLOAT
        elif isinstance(value, str):
            if value.startswith('[') and value.endswith(']'):
                _type = cls.LIST
            elif value.startswith('{') and value.endswith('}'):
                _type = cls.DICTIONARY

        return _type