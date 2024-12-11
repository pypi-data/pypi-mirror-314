from typing import Optional

from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType


class DataFormat:
    def __init__(self, data_type:Optional[DataType]=None, justify_type:Optional[JustifyType] = JustifyType.LEFT, decimal_places:Optional[int]=2, decimal_places_of_zero:Optional[int] = 1):
        """
        数据格式
        :param data_type: 数据类型
        :param justify_type: 对齐方式
        :param decimal_places: 小数位数
        :param decimal_places_of_zero: 小数为0时的小数位数
        """
        self.data_type = data_type
        self.justify_type = justify_type
        self.decimal_places = decimal_places if data_type == DataType.FLOAT else 0
        self.decimal_places_of_zero = decimal_places_of_zero if data_type == DataType.FLOAT else 0

    def __str__(self):
        """
        返回 DataFormat 实例的字符串表示。
        :return: DataFormat 实例的字符串表示。 """
        return f"DataFormat({', '.join(f'{key}={value}' for key, value in vars(self).items())})"