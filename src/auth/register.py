from PySide6.QtCore import Qt, Slot, Signal, QSize
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton
from PySide6.QtGui import QIcon

from src.db.database import Database
from src.db.init_db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from src.db.exec_select import departments

from src.auth.hash_password import hash_password
from src.window_methods import load_font

from src.auth.auth_methods import Auth


class RegisterWindow(QWidget):
    registration_successful = Signal()

    def __init__(self, root, login_window=None):
        super().__init__()
        self.setWindowTitle('Система для работы с ОХЛП')

        self.db = Database(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )

        self.root = root
        self.login_window = login_window
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

        self.greeting_lbl = QLabel('Добро пожаловать!\nЗарегистрируйтесь для работы с системой')
        self.greeting_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.greeting_lbl.setFont(title_font)

        self.lastname_lbl = QLabel('Фамилия')
        self.lastname_lbl.setFont(label_font)
        self.lastname_field = QLineEdit()
        self.lastname_field.setFont(label_font)

        self.firstname_lbl = QLabel('Имя')
        self.firstname_lbl.setFont(label_font)
        self.firstname_field = QLineEdit()
        self.firstname_field.setFont(label_font)

        self.patronymic_lbl = QLabel('Отчество (при наличии)')
        self.patronymic_lbl.setFont(label_font)
        self.patronymic_field = QLineEdit()
        self.patronymic_field.setFont(label_font)

        self.email = QLabel('Электронная почта')
        self.email.setFont(label_font)
        self.email_field = QLineEdit()
        self.email_field.setFont(label_font)

        self.department_lbl = QLabel('Отдел')
        self.department_lbl.setFont(label_font)
        self.department_combo = QComboBox()
        self.department_combo.addItems(departments)
        self.department_combo.setFont(label_font)

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

        self.confirm_open_password_btn = QPushButton()
        self.confirm_open_password_btn.setIcon(self.open_eye_icon)
        self.confirm_open_password_btn.setIconSize(QSize(15, 15))
        self.confirm_open_password_btn.setStyleSheet('background-color: #F5F5F7;')
        self.confirm_open_password_btn.clicked.connect(
            lambda: self.auth_methods.toggle_password_visibility(self.confirm_open_password_btn,
                                                                 self.confirm_password_field,
                                                                 self.open_eye_icon,
                                                                 self.close_eye_icon,
                                                                 label_font))

        self.password_lbl = QLabel('Пароль')
        self.password_lbl.setFont(label_font)
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_lbl = QLabel('Подтверждение пароля')
        self.confirm_password_lbl.setFont(label_font)
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.open_password_btn)

        confirm_password_layout = QHBoxLayout()
        confirm_password_layout.addWidget(self.confirm_password_field)
        confirm_password_layout.addWidget(self.confirm_open_password_btn)

        self.register_btn = QPushButton('Зарегистрироваться')
        self.register_btn.setFont(btn_font)

        self.login_lbl = QLabel('Уже есть аккаунт?')
        self.login_lbl.setFont(label_font)
        self.login_btn = QPushButton('Войти')
        self.login_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        greeting_layout = QHBoxLayout()
        greeting_layout.addWidget(self.greeting_lbl)
        greeting_layout.addWidget(self.theme_btn)

        self.layout.addLayout(greeting_layout)

        self.layout.addWidget(self.lastname_lbl)
        self.layout.addWidget(self.lastname_field)

        self.layout.addWidget(self.firstname_lbl)
        self.layout.addWidget(self.firstname_field)

        self.layout.addWidget(self.patronymic_lbl)
        self.layout.addWidget(self.patronymic_field)

        self.layout.addWidget(self.email)
        self.layout.addWidget(self.email_field)

        self.layout.addWidget(self.department_lbl)
        self.layout.addWidget(self.department_combo)

        self.layout.addWidget(self.password_lbl)
        self.layout.addLayout(password_layout)

        self.layout.addWidget(self.confirm_password_lbl)
        self.layout.addLayout(confirm_password_layout)

        self.layout.addStretch()

        self.layout.addWidget(self.register_btn)

        self.layout.addWidget(self.login_lbl)
        self.layout.addWidget(self.login_btn)

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
            self.lastname_field.text(),
            self.firstname_field.text(),
            self.email_field.text(),
            self.password_field.text(),
            self.confirm_password_field.text()
        ])

    def register_user(self):
        lastname = self.lastname_field.text()
        firstname = self.firstname_field.text()
        patronymic = self.patronymic_field.text()
        email = self.email_field.text()
        department = self.department_combo.currentText()
        password = self.password_field.text()

        hashed_password = hash_password(password)
        self.db.insert_users(lastname, firstname, patronymic, email, hashed_password)

        department_id = self.db.select_department_id(department)
        user_id = self.db.select_user_id(email)
        self.db.insert_users_departments(user_id, department_id)

        self.auth_methods.show_message('Регистрация прошла успешно!')
        self.registration_successful.emit()

    @Slot()
    def register(self):
        email = self.email_field.text()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()

        if self.db.check_user_exists(email):
            self.auth_methods.show_warning('Пользователь уже существует')
            return

        if not self.check_not_empty():
            self.auth_methods.show_warning('Заполните все поля')
            return

        if not self.auth_methods.email_check(email):
            self.auth_methods.show_warning('Неверный формат электронной почты')
            return

        if password != confirm_password:
            self.auth_methods.show_warning('Пароли не совпадают')
            return

        self.register_user()

