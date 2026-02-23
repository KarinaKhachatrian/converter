import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.auth.register import RegisterWindow
from src.auth.login import LoginWindow
from src.account.account_window import AccountWindow
from src.pdf_processor.pdf_processor_window import ProcessorWindow

from src.window_methods import show_window, switch_window

if __name__ == '__main__':
    app = QApplication([])

    current_file = Path(__file__).resolve()
    root = current_file.parents[1] / 'src'

    register_window = RegisterWindow(root)
    register_window.resize(800, 600)

    login_window = LoginWindow(root)
    login_window.resize(800, 400)

    account_window = AccountWindow(root)
    account_window.resize(700, 300)

    pdf_processor_window = ProcessorWindow(root)
    pdf_processor_window.resize(800, 700)

    register_window.login_window = login_window
    login_window.register_window = register_window

    with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
        style_sheet = f.read()
        register_window.setStyleSheet(style_sheet)
        login_window.setStyleSheet(style_sheet)
        account_window.setStyleSheet(style_sheet)
        pdf_processor_window.setStyleSheet(style_sheet)

    show_window(register_window)


    register_window.register_btn.clicked.connect(register_window.register)
    login_window.login_btn.clicked.connect(login_window.login)

    register_window.registration_successful.connect(
        lambda: switch_window(register_window, login_window)
    )
    login_window.login_successful.connect(
        lambda: switch_window(login_window, account_window)
    )

    register_window.login_btn.clicked.connect(
        lambda: switch_window(register_window, login_window)
    )
    login_window.register_btn.clicked.connect(
        lambda: switch_window(login_window, register_window)
    )

    account_window.convert_btn.clicked.connect(
        lambda: switch_window(account_window, pdf_processor_window)
    )
    pdf_processor_window.back_btn.clicked.connect(
        lambda: switch_window(pdf_processor_window, account_window)
    )

    sys.exit(app.exec())