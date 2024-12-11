from enum import Enum
from typing import Optional


class FunctionStatus(Enum):
    NORMAL = (1, "正常")  # 活动状态，可执行
    CLOSED = (0, "关闭")  # 关闭状态
    LOCKED = (9, "冻结")  # 暂停使用


    def __init__(self, value:Optional[int], description:Optional[str]):
        self.value = value
        self.description = description