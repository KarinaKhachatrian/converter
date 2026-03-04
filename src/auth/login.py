import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from src.db.database import Database

from src.auth.hash_password import hash_password
from src.auth.load_fonts import load_font

from src.auth.auth_methods import AuthMethods

class LoginWindow(QWidget):
    login_successful = Signal()

    def __init__(self, root, register_window=None):
        super().__init__()
        self.setWindowTitle("Система для работы с ОХЛП")

        self.db = Database(
            dbname="rls",
            user="postgres",
            password="postgres",
            host="localhost"
        )

        self.register_window = register_window

        self.auth_methods = AuthMethods()

        self.greeting_lbl = QLabel('Добро пожаловать!')
        self.greeting_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.greeting_lbl.setFont(title_font)

        self.email = QLabel('Электронная почта')
        self.email.setFont(label_font)
        self.email_field = QLineEdit()
        self.email_field.setFont(label_font)

        self.password_lbl = QLabel('Пароль')
        self.password_lbl.setFont(label_font)
        self.password_field = QLineEdit()
        self.password_field.setFont(label_font)
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton('Войти')
        self.login_btn.setFont(btn_font)

        self.register_lbl = QLabel('Ещё нет аккаунта?')
        self.register_lbl.setFont(label_font)
        self.register_btn = QPushButton('Зарегистрироваться')
        self.register_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addWidget(self.greeting_lbl)
        self.layout.addStretch()

        self.layout.addWidget(self.email)
        self.layout.addWidget(self.email_field)

        self.layout.addWidget(self.password_lbl)
        self.layout.addWidget(self.password_field)

        self.layout.addStretch()

        self.layout.addWidget(self.login_btn)

        self.layout.addWidget(self.register_lbl)
        self.layout.addWidget(self.register_btn)

    @Slot()
    def login(self) -> None:
        email = self.email_field.text()
        password = self.password_field.text()

        if not (self.auth_methods.empty_field_check(email) and
                self.auth_methods.empty_field_check(password)):

            if not(self.auth_methods.len_field_check(email) and
                self.auth_methods.len_field_check(password)):

                if self.db.check_credentials(email, hash_password(password)):
                    self.auth_methods.show_message('Аутентификация прошла успешно!')
                    self.login_successful.emit()
                else:
                    self.auth_methods.show_warning('Неверный логин или пароль')
            else:
                self.auth_methods.show_warning('Введённые данные не могут быть короче 1 символа')
        else:
            self.auth_methods.show_warning('Заполните все поля')

    def get_email(self) -> str:
        return self.email_field.text()


# if __name__ == "__main__":
#     app = QApplication([])
#
#     current_file = Path(__file__).resolve()
#     root = current_file.parents[1]
#
#     widget = LoginWindow(root)
#
#     with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
#         style_sheet = f.read()
#         widget.setStyleSheet(style_sheet)
#
#     widget.resize(800, 400)
#     widget.show()
#
#     sys.exit(app.exec())