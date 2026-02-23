from PySide6.QtWidgets import QWidget

def show_window(window: QWidget) -> None:
    window.show()

def switch_window(current_window: QWidget, change_window: QWidget) -> None:
    change_window.show()
    current_window.close()