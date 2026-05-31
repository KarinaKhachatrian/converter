from pathlib import Path
from PySide6.QtCore import Qt, Slot, Signal, QSize
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QIcon

from src.db.database import Database
from src.db.init_db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

from src.auth.hash_password import hash_password
from src.window_methods import load_font

from src.auth.auth_methods import Auth
from src.get_base_path import get_base_path


class LoginWindow(QWidget):
    login_successful = Signal()

    def __init__(self, root, register_window=None):
        super().__init__()
        self.setWindowTitle('Система для работы с ОХЛП')

        self.db = Database(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

        self.base_path = Path(get_base_path())
        self.root = self.base_path / 'src'

        self.register_window = register_window
        self.auth_methods = Auth()

        self.open_eye_icon = QIcon(str(self.root / 'icons/open_eye.png'))
        self.close_eye_icon = QIcon(str(self.root / 'icons/close_eye.png'))

        self.light_icon = QIcon(str(self.root / 'icons/sun.png'))
        self.dark_icon = QIcon(str(self.root / 'icons/moon.png'))
        self.is_light_theme = True

        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(QSize(35, 35))
        self.theme_btn.setIcon(self.light_icon)
        self.theme_btn.setIconSize(QSize(25, 25))
        self.theme_btn.setStyleSheet('background-color: #F5F5F7;')
        self.theme_btn.clicked.connect(self.change_theme)

        self.greeting_lbl = QLabel('Добро пожаловать!\nВойдите в свой аккаунт для работы с системой')
        self.greeting_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_font_path = str(self.root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(self.root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(self.root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.greeting_lbl.setFont(title_font)

        self.email = QLabel('Электронная почта')
        self.email.setFont(label_font)
        self.email_field = QLineEdit()
        self.email_field.setFont(label_font)

        self.open_password_btn = QPushButton()
        self.open_password_btn.setIcon(self.open_eye_icon)
        self.open_password_btn.setIconSize(QSize(15, 15))
        self.open_password_btn.setStyleSheet('background-color: #F5F5F7;')
        self.open_password_btn.clicked.connect(
            lambda: self.auth_methods.toggle_password_visibility(self.open_password_btn,
                                                                 self.password_field,
                                                                 self.open_eye_icon,
                                                                 self.close_eye_icon,
                                                                 label_font))

        self.password_lbl = QLabel('Пароль')
        self.password_lbl.setFont(label_font)
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.open_password_btn)

        self.login_btn = QPushButton('Войти')
        self.login_btn.setFont(btn_font)

        self.register_lbl = QLabel('Ещё нет аккаунта?')
        self.register_lbl.setFont(label_font)
        self.register_btn = QPushButton('Зарегистрироваться')
        self.register_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        greeting_layout = QHBoxLayout()
        greeting_layout.addWidget(self.greeting_lbl)
        greeting_layout.addWidget(self.theme_btn)

        self.layout.addLayout(greeting_layout)

        self.layout.addWidget(self.email)
        self.layout.addWidget(self.email_field)

        self.layout.addWidget(self.password_lbl)
        #self.layout.addWidget(self.password_field)
        self.layout.addLayout(password_layout)

        self.layout.addStretch()

        self.layout.addWidget(self.login_btn)

        self.layout.addWidget(self.register_lbl)
        self.layout.addWidget(self.register_btn)

    def change_theme(self):
        widget = self
        if self.is_light_theme:
            with open(self.root / r'styles/dark.qss', 'r', encoding='utf-8') as f:
                dark_theme = f.read()
                widget.setStyleSheet(dark_theme)
            self.theme_btn.setIcon(self.dark_icon)
            self.is_light_theme = False
        else:
            with open(self.root / r'styles/light.qss', 'r', encoding='utf-8') as f:
                light_theme = f.read()
                widget.setStyleSheet(light_theme)
            self.theme_btn.setIcon(self.light_icon)
            self.is_light_theme = True

    def check_not_empty(self):
        return all([
            self.email_field.text(),
            self.password_field.text(),
        ])

    def login_user(self):
        self.auth_methods.show_message('Аутентификация прошла успешно!')
        self.login_successful.emit()

    @Slot()
    def login(self):
        email = self.email_field.text()
        password = self.password_field.text()

        if not self.check_not_empty():
            self.auth_methods.show_warning('Заполните все поля')
            return

        elif not self.db.check_credentials(email, hash_password(password)):
            self.auth_methods.show_warning('Неверный логин или пароль')

        else:
            self.login_user()

