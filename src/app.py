import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.auth.register import RegisterWindow
from src.auth.login import LoginWindow

from src.window_methods import show_window, switch_window

if __name__ == '__main__':
    app = QApplication([])

    current_file = Path(__file__).resolve()
    root = current_file.parents[1] / 'src'

    register_window = RegisterWindow(root)
    register_window.resize(800, 600)

    login_window = LoginWindow(root)
    login_window.resize(800, 400)

    with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
        style_sheet = f.read()
        register_window.setStyleSheet(style_sheet)
        login_window.setStyleSheet(style_sheet)

    show_window(register_window)

    register_window.login_btn.clicked.connect(lambda: switch_window(register_window, login_window))
    login_window.register_btn.clicked.connect(lambda: switch_window(login_window, register_window))

    sys.exit(app.exec())