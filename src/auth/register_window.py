import os
import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QComboBox
from PySide6.QtGui import QFont

class RegisterWindow(QWidget):
   def __init__(self):
       super().__init__()

       self.greeting_lbl = QLabel('Добро пожаловать!\nЗарегистрируйтесь для работы с системой')
       self.greeting_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

       title_font = QFont("Fira Sans", 16, QFont.Weight.Bold)
       label_font = QFont("Fira Sans", 10)
       btn_font = QFont("Fira Sans", 11, QFont.Weight.Bold)

       self.greeting_lbl.setFont(title_font)

       self.lastname_lbl = QLabel('Фамилия')
       self.lastname_lbl.setFont(label_font)
       self.lastname_field = QLineEdit()
       self.lastname_field.setFont(QFont("Fira Sans", 10))

       self.firstname_lbl = QLabel('Имя')
       self.firstname_lbl.setFont(label_font)
       self.firstname_field = QLineEdit()
       self.firstname_field.setFont(QFont("Fira Sans", 10))

       self.patronymic_lbl = QLabel('Отчество')
       self.patronymic_lbl.setFont(label_font)
       self.patronymic_field = QLineEdit()
       self.patronymic_field.setFont(QFont("Fira Sans", 10))

       self.email = QLabel('Электронная почта')
       self.email.setFont(label_font)
       self.email_field = QLineEdit()
       self.email_field.setFont(QFont("Fira Sans", 10))

       self.department_lbl = QLabel('Отдел')
       self.department_lbl.setFont(label_font)
       self.department_combo = QComboBox()
       self.department_combo.addItems([
           "Отдел IT", "Отдел менеджеров", "Отдел HR", "Отдел библиомед", "Отдел администрации"
       ])
       self.department_combo.setFont(QFont("Fira Sans", 10))

       self.password = QLabel('Пароль')
       self.password.setFont(label_font)
       self.password_field = QLineEdit()
       self.password_field.setFont(QFont("Fira Sans", 10))
       self.password_field.setEchoMode(QLineEdit.EchoMode.Password)

       self.register_btn = QPushButton('Зарегистрироваться')
       self.register_btn.setFont(btn_font)

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

       self.layout.addWidget(self.password)
       self.layout.addWidget(self.password_field)

       self.layout.addStretch()

       self.layout.addWidget(self.register_btn)
       self.register_btn.clicked.connect(self.register)

   @Slot()
   def register(self):
       pass

if __name__ == "__main__":
    app = QApplication(['Система для работы с ОХЛП'])

    widget = RegisterWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())


