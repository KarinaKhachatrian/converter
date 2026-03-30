import sys
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLineEdit, QPlainTextEdit

from src.auth.load_fonts import load_font
from src.db.database import Database


class CRUDWindow(QWidget):
    def __init__(self, root, user_id):
        super().__init__()
        self.user_id = user_id

        self.db = Database(
            dbname="rls",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        filenames = self.db.select_filenames(self.user_id)

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        icon = QIcon('icons/back_icon.png')

        self.setWindowTitle("Система для работы с ОХЛП")

        self.demonstration_lbl = QLabel('Просмотр и редактирование данных')
        self.demonstration_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.demonstration_lbl.setFont(title_font)

        self.filename_lbl = QLabel('Файл ОХЛП')
        self.filename_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filename_lbl.setFont(title_font)

        self.filenames_combo = QComboBox(self)
        self.filenames_combo.addItems(filenames)
        self.filenames_combo.setFont(label_font)
        self.filenames_combo.currentTextChanged.connect(self.change_filename)

        self.current_filename = self.filenames_combo.currentText()

        second_level_headers = self.db.select_second_level_headers(self.current_filename)
        third_level_headers = self.db.select_third_level_headers(self.current_filename)

        self.second_content_btn = QPushButton('Заголовок второго уровня')
        self.second_content_btn.clicked.connect(self.show_second_level_content)
        self.second_content_btn.setFont(btn_font)

        self.third_content_btn = QPushButton('Заголовок третьего уровня')
        self.third_content_btn.clicked.connect(self.show_third_level_content)
        self.third_content_btn.setFont(btn_font)

        btn_layout = QHBoxLayout()

        btn_layout.addWidget(self.second_content_btn)
        btn_layout.addWidget(self.third_content_btn)

        self.second_combo = QComboBox(self)
        self.second_combo.addItems(second_level_headers)
        self.second_combo.setFont(label_font)
        self.second_combo.setVisible(False)

        self.third_combo = QComboBox(self)
        self.third_combo.addItems(third_level_headers)
        self.third_combo.setFont(label_font)
        self.third_combo.setVisible(False)

        self.show_btn = QPushButton('Показать данные')
        self.show_btn.setFont(btn_font)
        self.show_btn.setIcon(icon)
        self.show_btn.setIconSize(QSize(30, 30))
        self.show_btn.clicked.connect(self.show_content)

        # self.content_line = QLineEdit()
        # self.content_line.setFont(label_font)
        self.content_plain = QPlainTextEdit()
        self.content_plain.setReadOnly(True)
        self.content_plain.setFont(label_font)

        self.back_btn = QPushButton('Назад')
        self.back_btn.setFont(btn_font)
        self.back_btn.setIcon(icon)
        self.back_btn.setIconSize(QSize(30, 30))

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addWidget(self.demonstration_lbl)

        self.layout.addWidget(self.filename_lbl)
        self.layout.addWidget(self.filenames_combo)

        self.layout.addLayout(btn_layout)

        self.layout.addWidget(self.second_combo)
        self.layout.addWidget(self.third_combo)

        self.layout.addWidget(self.show_btn)
        self.layout.addWidget(self.content_plain)

        self.layout.addStretch()

        self.layout.addWidget(self.back_btn)

    def change_filename(self, new_filename):
        self.current_filename = new_filename

        second_level_headers = self.db.select_second_level_headers(self.current_filename)
        third_level_headers = self.db.select_third_level_headers(self.current_filename)

        self.second_combo.clear()
        self.second_combo.addItems(second_level_headers)

        self.third_combo.clear()
        self.third_combo.addItems(third_level_headers)

        self.content_plain.clear()


    def show_second_level_content(self):
        self.second_combo.setVisible(True)
        self.third_combo.setVisible(False)

    def show_third_level_content(self):
        self.third_combo.setVisible(True)
        self.second_combo.setVisible(False)

    def show_content(self):
        if self.second_combo.isVisible():
            second_header = self.second_combo.currentText()
            second_content = self.db.select_second_level_content(second_header, self.current_filename)
            self.content_plain.setPlainText(second_content)
        else:
            third_header = self.third_combo.currentText()
            third_content = self.db.select_third_level_content(third_header, self.current_filename)
            self.content_plain.setPlainText(third_content)


if __name__ == "__main__":
    app = QApplication([])

    current_file = Path(__file__).resolve()
    root = current_file.parents[1]

    widget = CRUDWindow(root, '1')

    with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
        style_sheet = f.read()
        widget.setStyleSheet(style_sheet)

    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())