import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from src.auth.load_fonts import load_font


class AccountWindow(QWidget):
    def __init__(self, root):
        super().__init__()
        self.setWindowTitle("Система для работы с ОХЛП")

        self.greeting_lbl = QLabel('Добро пожаловать!')
        self.greeting_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.greeting_lbl.setFont(title_font)

        self.question_lbl = QLabel('Выберите задачу для выполнения\n')
        self.question_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_lbl.setFont(label_font)

        self.convert_btn = QPushButton('Конвертация файлов ОХЛП')
        self.convert_btn.setFont(btn_font)

        self.db_btn = QPushButton('Работа с базой данных')
        self.db_btn.setFont(btn_font)

        self.stamps_btn = QPushButton('Просмотр и редактирование')
        self.stamps_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addWidget(self.greeting_lbl)
        self.layout.addStretch()

        self.layout.addWidget(self.question_lbl)
        self.layout.addStretch()

        self.layout.addWidget(self.convert_btn)
        self.layout.addWidget(self.db_btn)
        self.layout.addWidget(self.stamps_btn)

# if __name__ == "__main__":
#     app = QApplication([])
#
#     current_file = Path(__file__).resolve()
#     root = current_file.parents[1]
#
#     widget = AccountWindow(root)
#
#     with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
#         style_sheet = f.read()
#         widget.setStyleSheet(style_sheet)
#
#     widget.resize(700, 300)
#     widget.show()
#
#     sys.exit(app.exec())