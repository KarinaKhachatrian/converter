from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont, QFontDatabase

def show_window(window: QWidget) -> None:
    window.show()

def switch_window(current_window: QWidget, change_window: QWidget) -> None:
    change_window.show()
    current_window.close()

def load_font(font_path: str, font_size: int) -> QFont:
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    font = QFont(font_families[0], font_size)
    return font