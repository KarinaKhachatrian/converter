import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from src.auth.load_fonts import load_font


class ModelWindow(QWidget):
    def __init__(self, root):
        super().__init__()

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.setWindowTitle("Система для работы с ОХЛП")

        self.demonstration_lbl = QLabel('Демонстрация работы модели обнаружения штампов')
        self.demonstration_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.demonstration_lbl.setFont(title_font)

        self.choose_lbl = QLabel("Выберите файл ОХЛП")
        self.choose_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_lbl.setFont(label_font)

        self.choose_btn = QPushButton("Выбрать директорию")
        self.choose_btn.setFont(btn_font)

        self.demonstrate_btn = QPushButton('Обнаружить штамп')
        self.demonstrate_btn.setFont(btn_font)

        self.back_btn = QPushButton("Назад")
        self.back_btn.setFont(btn_font)
        icon = QIcon('icons/back_icon.png')
        self.back_btn.setIcon(icon)
        self.back_btn.setIconSize(QSize(30, 30))

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addWidget(self.demonstration_lbl)
        self.layout.addWidget(self.choose_lbl)
        self.layout.addWidget(self.choose_btn)
        self.layout.addWidget(self.demonstrate_btn)
        self.layout.addWidget(self.back_btn)
        self.layout.addStretch()

if __name__ == "__main__":
    app = QApplication([])

    current_file = Path(__file__).resolve()
    root = current_file.parents[1]

    widget = ModelWindow(root)

    with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
        style_sheet = f.read()
        widget.setStyleSheet(style_sheet)

    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())