from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QPlainTextEdit

from src.window_methods import load_font
from src.db.database import Database
from src.db.init_db import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


class ReadWindow(QWidget):
    def __init__(self, root, user_id):
        super().__init__()
        
        self.root = root
        self.user_id = user_id

        self.db = Database(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        filenames = self.db.select_filenames(self.user_id)

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        title_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Bold.ttf')
        title_font = load_font(title_font_path, 15)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        back_icon = QIcon('icons/back_icon.png')

        self.light_icon = QIcon(str(self.root / 'icons/sun.png'))
        self.dark_icon = QIcon(str(self.root / 'icons/moon.png'))
        self.is_light_theme = True

        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(QSize(35, 35))
        self.theme_btn.setIcon(self.light_icon)
        self.theme_btn.setIconSize(QSize(25, 25))
        self.theme_btn.setStyleSheet('background-color: #F5F5F7;')
        self.theme_btn.clicked.connect(self.change_theme)

        self.setWindowTitle('Система для работы с ОХЛП')

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

        greeting_layout = QHBoxLayout()
        greeting_layout.addWidget(self.demonstration_lbl)
        greeting_layout.addWidget(self.theme_btn)

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
        self.show_btn.setIconSize(QSize(30, 30))
        self.show_btn.clicked.connect(self.show_content)

        self.content_plain = QPlainTextEdit()
        self.content_plain.setReadOnly(True)
        self.content_plain.setFont(label_font)

        self.back_btn = QPushButton('Назад')
        self.back_btn.setFont(btn_font)
        self.back_btn.setIcon(back_icon)
        self.back_btn.setIconSize(QSize(30, 30))

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        self.layout.addLayout(greeting_layout)

        self.layout.addWidget(self.filename_lbl)
        self.layout.addWidget(self.filenames_combo)

        self.layout.addLayout(btn_layout)

        self.layout.addWidget(self.second_combo)
        self.layout.addWidget(self.third_combo)

        self.layout.addWidget(self.show_btn)
        self.layout.addWidget(self.content_plain)

        self.layout.addStretch()

        self.layout.addWidget(self.back_btn)

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

