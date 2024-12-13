from mag_tools.model.common.justify_type import JustifyType
from mag_tools.model.common.data_type import DataType

from mag_tools.bean.common.data_format import DataFormat
from mag_tools.utils.common.string_format import StringFormat
import unittest

class TestStringFormat(unittest.TestCase):
    def test_pad_string(self):
        # 测试右对齐
        self.assertEqual(StringFormat.pad_string("test", 10, JustifyType.RIGHT), "      test")
        # 测试居中对齐
        self.assertEqual(StringFormat.pad_string("test", 10, JustifyType.CENTER), "   test   ")
        # 测试左对齐
        self.assertEqual(StringFormat.pad_string("test", 10, JustifyType.LEFT), "test      ")
        # 测试字符串长度大于目标长度
        self.assertEqual(StringFormat.pad_string("test", 2, JustifyType.RIGHT), "test")

    def test_pad_strings(self):
        # 测试多个字符串右对齐
        strings = ["test1", "test2", "test3"]
        expected_output = "     test1     test2     test3"
        self.assertEqual(expected_output, StringFormat.pad_strings(strings,  10, JustifyType.RIGHT))
        # 测试多个字符串居中对齐
        expected_output = " test1   test2   test3  "
        self.assertEqual(expected_output, StringFormat.pad_strings(strings, 8, JustifyType.CENTER))
        # 测试多个字符串左对齐
        expected_output = "test1 test2 test3"
        self.assertEqual(expected_output, StringFormat.pad_strings(strings, 5, JustifyType.LEFT))

    def test_format_number(self):
        # 测试整数格式化
        data_format = DataFormat(DataType.INTEGER)
        self.assertEqual("123", StringFormat.format_number(123, data_format))

        # 测试浮点数格式化
        data_format = DataFormat(DataType.FLOAT, decimal_places=2, decimal_places_of_zero=2)
        self.assertEqual("123.46", StringFormat.format_number(123.456, data_format))
        self.assertEqual("123.00", StringFormat.format_number(123.0, data_format))

        # 测试科学计数法格式化
        data_format = DataFormat(DataType.FLOAT, decimal_places=5, scientific=True)
        self.assertEqual(StringFormat.format_number(1e9, data_format), "1.00000e9")
        self.assertEqual(StringFormat.format_number(1e-4, data_format), "1.00000e-4")

        # 测试非数值类型
        self.assertEqual(StringFormat.format_number("text", data_format), "text")

if __name__ == '__main__':
    unittest.main()
