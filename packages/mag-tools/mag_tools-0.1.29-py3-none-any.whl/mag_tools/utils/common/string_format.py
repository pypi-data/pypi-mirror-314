from mag_tools.model.common.data_type import DataType

from mag_tools.model.common.justify_type import JustifyType


class StringFormat:
    @staticmethod
    def pad_string(string, pad_length, justify_type=JustifyType.RIGHT):
        """
        将字符串用空格补充到指定长度，空格添加在字符串前。
        参数：
        :param justify_type: 对齐方式，空格补齐
        :param string: 原始字符串
        :param pad_length: 目标长度
        :return: 补充空格后的字符串
        """
        string = str(string) if DataType.get_type(string) != DataType.STRING else string

        if len(string) >= pad_length:
            return string

        padding_length = pad_length - len(string)
        if justify_type == JustifyType.RIGHT:
            return ' ' * padding_length + string
        elif justify_type == JustifyType.CENTER:
            left_padding = padding_length // 2
            right_padding = padding_length - left_padding
            return ' ' * left_padding + string + ' ' * right_padding
        else:
            return string + ' ' * padding_length

    @staticmethod
    def pad_strings(strings, separator, pad_length, justify_type=JustifyType.RIGHT):
        strings = [StringFormat.pad_string(string, pad_length, justify_type) + separator for string in strings]
        return ''.join(strings)