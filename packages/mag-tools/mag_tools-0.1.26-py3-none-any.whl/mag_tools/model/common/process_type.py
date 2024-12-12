from enum import Enum

class ProcessStatus(Enum):
    UNKNOWN = ("UNKNOWN", "未知")
    TO_BE_CONFIRM = ("TO_BE_CONFIRM", "待确认")
    PENDING = ("PENDING", "待处理")
    PROCESSING = ("PROCESSING", "处理中")
    SUCCESS = ("SUCCESS", "成功")
    FAIL = ("FAIL", "失败")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def get_by_desc(cls, description: str):
        for status in cls:
            if status.description == description:
                return status
        return None
