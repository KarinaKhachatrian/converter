import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMessageBox

from src.db.database import Database

from src.auth.register import RegisterWindow
from src.auth.login import LoginWindow
from src.account.account_window import AccountWindow
from src.pdf_processor.pdf_processor_window import ProcessorWindow

from src.window_methods import show_window, switch_window
from src.structurer.structurer_window import DBWorkWindow
from src.read.read_window import ReadWindow

class Application:
    def __init__(self):
        self.app = QApplication([])
        current_file = Path(__file__).resolve()
        self.root = current_file.parents[1] / 'src'
        self.db = Database(
            dbname="rls",
            user="postgres",
            password="postgres",
            host="localhost"
        )

        with open(self.root / r"styles/light.qss", "r", encoding="utf-8") as f:
            self.style_sheet = f.read()

        self.db_work_window = None
        self.register_window = None
        self.login_window = None
        self.account_window = None
        self.pdf_processor_window = None
        self.read_window = None

    def setup_windows(self):
        self.register_window = RegisterWindow(self.root)
        self.register_window.resize(800, 600)
        self.register_window.setStyleSheet(self.style_sheet)

        self.login_window = LoginWindow(self.root)
        self.login_window.resize(800, 400)
        self.login_window.setStyleSheet(self.style_sheet)

        self.account_window = AccountWindow(self.root)
        self.account_window.resize(700, 300)
        self.account_window.setStyleSheet(self.style_sheet)

        self.register_window.login_window = self.login_window
        self.login_window.register_window = self.register_window

    def setup_signals(self):
        self.register_window.register_btn.clicked.connect(self.register_window.register)
        self.login_window.login_btn.clicked.connect(self.login_window.login)

        self.register_window.registration_successful.connect(
            lambda: switch_window(self.register_window, self.login_window)
        )

        self.login_window.login_successful.connect(self.login_successful)

        self.register_window.login_btn.clicked.connect(
            lambda: switch_window(self.register_window, self.login_window)
        )
        self.login_window.register_btn.clicked.connect(
            lambda: switch_window(self.login_window, self.register_window)
        )

        self.account_window.db_btn.clicked.connect(self.db_btn_clicked)
        self.account_window.show_info_btn.clicked.connect(self.show_info_btn_clicked)

    def login_successful(self):
        email = self.login_window.get_email()
        user_id = self.db.select_user_id(email)

        self.db_work_window = DBWorkWindow(self.root, email)
        self.db_work_window.resize(800, 400)
        self.db_work_window.setStyleSheet(self.style_sheet)
        self.db_work_window.back_btn.clicked.connect(
            lambda: switch_window(self.db_work_window, self.account_window)
        )

        self.pdf_processor_window = ProcessorWindow(self.root, email)
        self.pdf_processor_window.resize(800, 700)
        self.pdf_processor_window.setStyleSheet(self.style_sheet)
        self.pdf_processor_window.back_btn.clicked.connect(
            lambda: switch_window(self.pdf_processor_window, self.account_window)
        )
        self.account_window.convert_btn.clicked.connect(
            lambda: switch_window(self.account_window, self.pdf_processor_window)
        )

        switch_window(self.login_window, self.account_window)

        self.read_window = ReadWindow(self.root, user_id)
        self.read_window.resize(800, 500)
        self.read_window.setStyleSheet(self.style_sheet)
        self.read_window.back_btn.clicked.connect(
            lambda: switch_window(self.read_window, self.account_window)
        )

    def db_btn_clicked(self):
        if self.db_work_window is not None:
            switch_window(self.account_window, self.db_work_window)
        else:
            QMessageBox.warning(self.account_window, "Ошибка",
                                "Сначала выполните вход в систему")

    def show_info_btn_clicked(self):
        if self.read_window is not None:
            switch_window(self.account_window, self.read_window)
        else:
            QMessageBox.warning(self.account_window, "Ошибка",
                                "Сначала выполните вход в систему")

    def run(self):
        self.setup_windows()
        self.setup_signals()

        show_window(self.register_window)
        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = Application()
    app.run()