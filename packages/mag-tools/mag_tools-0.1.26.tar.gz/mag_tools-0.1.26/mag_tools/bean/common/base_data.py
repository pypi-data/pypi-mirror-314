from typing import Optional, get_args

from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.bean.common.data_format import DataFormat
from mag_tools.model.common.justify_type import JustifyType


class BaseData:
    text_format: TextFormat
    data_formats: Optional[dict]

    def __init__(self):
        self.text_format = TextFormat(number_per_line=4, justify_type=JustifyType.LEFT, at_header='', decimal_places=4,
                                      decimal_places_of_zero=1)
        self.data_formats = None

    def get_data_formats(self) -> dict:
        members = vars(self)

        self.data_formats = {}
        for name, value in members.items():
            if name not in ['text_format', 'data_formats']:
                data_type = DataType.get_type(value)
                data_format = DataFormat(data_type, self.text_format.justify_type, self.text_format.decimal_places,
                                         self.text_format.decimal_places_of_zero)
                self.data_formats[name] = data_format
        return self.data_formats

class TestData(BaseData):
    def __init__(self, name:Optional[str]=None, age: Optional[int] = None, height: Optional[float] = None):
        super().__init__()

        self.name = name
        self.age = age
        self.height = height

if __name__ == '__main__':
    data = TestData(None, 12, 1)
    data_formats = data.get_data_formats()
    for name, data_format in data_formats.items():
        print(f"{name}: {data_format}")
