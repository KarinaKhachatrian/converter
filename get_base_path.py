import sys
import os

def get_base_path():
    """Получение корректного пути для ресурсов в exe"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
