from typing import Optional

from mag_tools.model.common.justify_type import JustifyType


class TextFormat:
    def __init__(self, number_per_line:Optional[int] = 1, justify_type:Optional[JustifyType] = JustifyType.LEFT, at_header:Optional[str] = '',
                 decimal_places:Optional[int]=2, decimal_places_of_zero:Optional[int] = 1):
        """
        数据格式
        :param number_per_line: 每行显示的数据个数
        :param justify_type: 对齐方式
        :param at_header: 句首添加的字符串
        :param decimal_places: 小数位数
        :param decimal_places_of_zero: 小数为0时的小数位数
        """
        self.number_per_line = number_per_line
        self.justify_type = justify_type
        self.at_header = at_header
        self.decimal_places = decimal_places if decimal_places is not None else 0
        self.decimal_places_of_zero = decimal_places_of_zero if decimal_places is not None else 0

    def __str__(self):
        """
        返回 TextFormat 实例的字符串表示。
        :return: TextFormat 实例的字符串表示。 """
        return f"TextFormat({', '.join(f'{key}={value}' for key, value in vars(self).items())})"