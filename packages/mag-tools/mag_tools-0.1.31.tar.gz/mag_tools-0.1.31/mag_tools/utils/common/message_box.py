import tkinter as tk
from tkinter import messagebox
from typing import Optional


class MessageBox:
    @staticmethod
    def showinfo(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Show an info message"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showinfo(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def showwarning(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Show a warning message"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showwarning(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def showerror(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Show an error message"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.showerror(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askquestion(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Ask a question"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askquestion(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askokcancel(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Ask if operation should proceed; return true if the answer is ok"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askokcancel(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askyesno(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Ask a question; return true if the answer is yes"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askyesno(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askyesnocancel(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Ask a question; return true if the answer is yes, None if cancelled."
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askyesnocancel(title, message)
        root.destroy()  # 销毁主窗口
        return res

    @staticmethod
    def askretrycancel(title:Optional[str]=None, message:Optional[str]=None, **options):
        "Ask if operation should be retried; return true if the answer is yes"
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        res = messagebox.askretrycancel(title, message)
        root.destroy()  # 销毁主窗口
        return res
