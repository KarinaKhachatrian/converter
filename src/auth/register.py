from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from src.db.database import Database
from src.db.exec_select import departments

from src.auth.hash_password import hash_password
from src.auth.load_fonts import load_font

from src.auth.auth_methods import AuthMethods

class RegisterWindow(QWidget):
    registration_successful = Signal()

    def __init__(self, root, login_window=None):
        super().__init__()
        self.setWindowTitle("Система для работы с ОХЛП")

        self.db = Database(
            dbname="rls",
            user="postgres",
            password="postgres",
            host="localhost"
        )

        self.login_window = login_window

        self.auth_methods = AuthMethods()

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

        self.password_lbl = QLabel('Пароль')
        self.password_lbl.setFont(label_font)
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_lbl = QLabel('Подтверждение пароля')
        self.confirm_password_lbl.setFont(label_font)
        self.confirm_password_field = QLineEdit()
        self.confirm_password_field.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_btn = QPushButton('Зарегистрироваться')
        self.register_btn.setFont(btn_font)

        self.login_lbl = QLabel('Уже есть аккаунт?')
        self.login_lbl.setFont(label_font)
        self.login_btn = QPushButton('Войти')
        self.login_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addWidget(self.greeting_lbl)
        self.layout.addStretch()

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
        self.layout.addWidget(self.password_field)

        self.layout.addWidget(self.confirm_password_lbl)
        self.layout.addWidget(self.confirm_password_field)

        self.layout.addStretch()

        self.layout.addWidget(self.register_btn)

        self.layout.addWidget(self.login_lbl)
        self.layout.addWidget(self.login_btn)


    @Slot()
    def register(self) -> None:
        lastname = self.lastname_field.text()
        firstname = self.firstname_field.text()
        patronymic = self.patronymic_field.text()
        email = self.email_field.text()
        department = self.department_combo.currentText()
        password = self.password_field.text()
        confirm_password = self.confirm_password_field.text()

        if not self.db.check_user_exists(email):
            if not (self.auth_methods.empty_field_check(lastname) or
                    self.auth_methods.empty_field_check(firstname) or
                    self.auth_methods.empty_field_check(email) or
                    self.auth_methods.empty_field_check(password) or
                    self.auth_methods.empty_field_check(confirm_password)):

                if not (self.auth_methods.len_field_check(lastname) or
                        self.auth_methods.len_field_check(firstname) or
                        self.auth_methods.len_field_check(email) or
                        self.auth_methods.len_field_check(password) or
                        self.auth_methods.len_field_check(confirm_password)):

                    if self.auth_methods.email_check(email):
                        if password == confirm_password:
                            hashed_password = hash_password(password)
                            self.db.insert_users(lastname, firstname, patronymic, email, hashed_password)

                            department_id = self.db.select_department_id(department)
                            user_id = self.db.select_user_id(email)
                            self.db.insert_users_departments(user_id, department_id)

                            self.auth_methods.show_message("Регистрация прошла успешно!")

                            self.registration_successful.emit()
                        else:
                            self.auth_methods.show_warning("Пароли не совпадают")
                    else:
                        self.auth_methods.show_warning("Неверный формат электронной почты")
                else:
                    self.auth_methods.show_warning("Введённые данные не могут быть короче 1 символа")
            else:
                self.auth_methods.show_warning("Заполните все поля")
        else:
            self.auth_methods.show_warning('Пользователь уже существует')


# if __name__ == "__main__":
#     app = QApplication([])
#
#     current_file = Path(__file__).resolve()
#     root = current_file.parents[1]
#
#     widget = RegisterWindow(root)
#
#     with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
#         style_sheet = f.read()
#         widget.setStyleSheet(style_sheet)
#
#     widget.resize(800, 600)
#     widget.show()
#
#     sys.exit(app.exec())

