from enum import Enum
from typing import Optional

class FunctionStatus(Enum):
    NORMAL = (1, "正常")  # 活动状态，可执行
    CLOSED = (0, "关闭")  # 关闭状态
    LOCKED = (9, "冻结")  # 暂停使用

    def __init__(self, code: Optional[int], description: Optional[str]):
        self.code = code
        self.description = description

    @classmethod
    def get_by_desc(cls, description: str):
        for status in cls:
            if status.description == description:
                return status
        return None
