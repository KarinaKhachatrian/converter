import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from src.auth.register import RegisterWindow
from src.auth.login import LoginWindow
from src.account.account_window import AccountWindow
from src.pdf_processor.pdf_processor_window import ProcessorWindow

from src.window_methods import show_window, switch_window
from src.structurer.structurer_window import DBWorkWindow


class Application:
    def __init__(self):
        self.app = QApplication([])
        self.db_work_window = None
        self.root = None
        self.register_window = None
        self.login_window = None
        self.account_window = None
        self.pdf_processor_window = None
        self.style_sheet = None

    def setup_windows(self):
        current_file = Path(__file__).resolve()
        self.root = current_file.parents[1] / 'src'

        self.register_window = RegisterWindow(self.root)
        self.register_window.resize(800, 600)

        self.login_window = LoginWindow(self.root)
        self.login_window.resize(800, 400)

        self.account_window = AccountWindow(self.root)
        self.account_window.resize(700, 300)

        self.pdf_processor_window = ProcessorWindow(self.root)
        self.pdf_processor_window.resize(800, 700)

        self.register_window.login_window = self.login_window
        self.login_window.register_window = self.register_window

        with open(self.root / r"styles/light.qss", "r", encoding="utf-8") as f:
            self.style_sheet = f.read()

    def setup_signals(self):
        self.register_window.register_btn.clicked.connect(self.register_window.register)
        self.login_window.login_btn.clicked.connect(self.login_window.login)

        self.register_window.registration_successful.connect(
            lambda: switch_window(self.register_window, self.login_window)
        )

        self.login_window.login_successful.connect(self.on_login_successful)

        self.register_window.login_btn.clicked.connect(
            lambda: switch_window(self.register_window, self.login_window)
        )
        self.login_window.register_btn.clicked.connect(
            lambda: switch_window(self.login_window, self.register_window)
        )

        self.account_window.convert_btn.clicked.connect(
            lambda: switch_window(self.account_window, self.pdf_processor_window)
        )

        self.account_window.db_btn.clicked.connect(self.on_db_btn_clicked)

        self.pdf_processor_window.back_btn.clicked.connect(
            lambda: switch_window(self.pdf_processor_window, self.account_window)
        )

    def on_login_successful(self):
        """Обработчик успешного входа"""
        email = self.login_window.get_email()

        self.db_work_window = DBWorkWindow(self.root, email)
        self.db_work_window.resize(800, 400)
        self.db_work_window.setStyleSheet(self.style_sheet)

        self.db_work_window.back_btn.clicked.connect(
            lambda: switch_window(self.db_work_window, self.account_window)
        )

        switch_window(self.login_window, self.account_window)

    def on_db_btn_clicked(self):
        if self.db_work_window is not None:
            switch_window(self.account_window, self.db_work_window)
        else:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self.account_window, "Ошибка",
                                "Сначала выполните вход в систему")

    def apply_styles(self):
        self.register_window.setStyleSheet(self.style_sheet)
        self.login_window.setStyleSheet(self.style_sheet)
        self.account_window.setStyleSheet(self.style_sheet)
        self.pdf_processor_window.setStyleSheet(self.style_sheet)

    def run(self):
        self.setup_windows()
        self.setup_signals()
        self.apply_styles()

        show_window(self.register_window)

        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = Application()
    app.run()