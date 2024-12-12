import tkinter as tk
from tkinter import messagebox
from typing import Optional


class MessageUtils:
    @staticmethod
    def message_box(message:Optional[str], title:Optional[str]='错误消息'):
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        messagebox.showinfo(title, message)
        root.mainloop()

if __name__ == '__main__':
    MessageUtils.message_box("消息")