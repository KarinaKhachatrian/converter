import re
from src.auth.regex import email_regex
from PySide6.QtWidgets import QMessageBox

class AuthMethods:
    @staticmethod
    def empty_field_check(field_text: str) -> bool:
        if field_text == '' or field_text.isspace():
            return True
        return False

    @staticmethod
    def len_field_check(field_text: str) -> bool:
        if len(field_text) <= 1:
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