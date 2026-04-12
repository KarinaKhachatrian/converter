import re

from PySide6.QtWidgets import QMessageBox, QLineEdit, QPushButton
from PySide6.QtGui import QIcon, QFont

from src.auth.regex import email_regex


class Auth:
    @staticmethod
    def empty_field_check(field_text: str) -> bool:
        if field_text == '' or field_text.isspace() or len(field_text) <= 1:
            return True
        return False

    @staticmethod
    def email_check(email: str) -> bool:
        if re.match(email_regex, email):
            return True
        return False

    @staticmethod
    def show_warning(warning_text: str) -> None:
        warning_msg = QMessageBox()
        warning_msg.warning(
            None,
            "Предупреждение",
            warning_text
        )
        warning_msg.show()

    @staticmethod
    def show_message(message_text: str) -> None:
        message_msg = QMessageBox()
        message_msg.information(
            None,
            "Информация",
            message_text
        )

    @staticmethod
    def toggle_password_visibility(password_btn: QPushButton,
                                   password_field: QLineEdit,
                                   open_icon_path: QIcon,
                                   close_icon_path: QIcon,
                                   font: QFont) -> None:

        if password_field.echoMode() == QLineEdit.EchoMode.Password:
            password_btn.setIcon(close_icon_path)
            password_field.setEchoMode(QLineEdit.EchoMode.Normal)
            password_field.setFont(font)
        else:
            password_btn.setIcon(open_icon_path)
            password_field.setEchoMode(QLineEdit.EchoMode.Password)

