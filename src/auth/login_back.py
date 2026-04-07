from PySide6.QtCore import QObject, Signal, Slot

from src.auth.hash_password import hash_password

class Login(QObject):
    login_successful = Signal(bool, str)

    def __init__(self, db, auth_methods):
        super().__init__()
        self.db = db
        self.auth_methods = auth_methods

    @Slot(str, str)
    def login_user(self, email, password):
        if (self.auth_methods.empty_field_check(email) or
                self.auth_methods.empty_field_check(password)):
            self.login_successful.emit(False, 'Заполните все поля')
            return

        if (self.auth_methods.len_field_check(email) or
                self.auth_methods.len_field_check(password)):
            self.login_successful.emit(False, 'Введённые данные не могут быть короче одного символа')
            return

        if self.db.check_credentials(email, hash_password(password)):
            self.auth_methods.show_message('Аутентификация прошла успешно!')
            self.login_successful.emit(True, '')
        else:
            self.auth_methods.show_warning('Неверный логин или пароль')

