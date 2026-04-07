from PySide6.QtCore import QObject, Signal, Slot

from src.auth.hash_password import hash_password


class Registration(QObject):
    registration_successful = Signal(bool, str)

    def __init__(self, db, auth_methods):
        super().__init__()
        self.db = db
        self.auth_methods = auth_methods

    @Slot(str, str, str, str, str, str, str)
    def register_user(self, lastname, firstname, patronymic, email,
                      department, password, confirm_password):

        if self.db.check_user_exists(email):
            self.registration_successful.emit(False, 'Пользователь уже существует')
            return

        if (self.auth_methods.empty_field_check(lastname) or
                self.auth_methods.empty_field_check(firstname) or
                self.auth_methods.empty_field_check(email) or
                self.auth_methods.empty_field_check(password) or
                self.auth_methods.empty_field_check(confirm_password)):
            self.registration_successful.emit(False, 'Заполните все поля')
            return

        if (self.auth_methods.len_field_check(lastname) or
                self.auth_methods.len_field_check(firstname) or
                self.auth_methods.len_field_check(email) or
                self.auth_methods.len_field_check(password) or
                self.auth_methods.len_field_check(confirm_password)):
            self.registration_successful.emit(False, 'Введённые данные не могут быть короче одного символа')
            return

        if self.auth_methods.email_check(email):
            if password == confirm_password:
                hashed_password = hash_password(password)
                self.db.insert_users(lastname, firstname, patronymic, email, hashed_password)

                department_id = self.db.select_department_id(department)
                user_id = self.db.select_user_id(email)
                self.db.insert_users_departments(user_id, department_id)

                self.auth_methods.show_message('Регистрация прошла успешно!')

                self.registration_successful.emit(True, '')
            else:
                self.auth_methods.show_warning('Пароли не совпадают')
                self.registration_successful.emit(False, 'Пароли не совпадают')
        else:
            self.auth_methods.show_warning('Неверный формат электронной почты')
            self.registration_successful.emit(False, 'Неверный формат электронной почты')


