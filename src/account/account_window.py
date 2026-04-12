from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon

from src.window_methods import load_font


class AccountWindow(QWidget):
    def __init__(self, root, username):
        super().__init__()

        self.root = root
        self.setWindowTitle('Система для работы с ОХЛП')

        self.light_icon = QIcon(str(self.root / 'icons/sun.png'))
        self.dark_icon = QIcon(str(self.root / 'icons/moon.png'))
        self.is_light_theme = True

        self.theme_btn = QPushButton()
        self.theme_btn.setFixedSize(QSize(35, 35))
        self.theme_btn.setIcon(self.light_icon)
        self.theme_btn.setIconSize(QSize(25, 25))
        self.theme_btn.setStyleSheet('background-color: #F5F5F7;')
        self.theme_btn.clicked.connect(self.change_theme)

        self.greeting_lbl = QLabel(f'Добро пожаловать, {username}!')
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

        self.show_info_btn = QPushButton('Просмотр структурированных данных')
        self.show_info_btn.setFont(btn_font)

        self.layout = QVBoxLayout(self)

        self.layout.setSpacing(10)
        self.layout.setContentsMargins(50, 30, 50, 30)

        greeting_layout = QHBoxLayout()
        greeting_layout.addWidget(self.greeting_lbl)
        greeting_layout.addWidget(self.theme_btn)

        self.layout.addLayout(greeting_layout)

        self.layout.addWidget(self.question_lbl)
        self.layout.addStretch()

        self.layout.addWidget(self.convert_btn)
        self.layout.addWidget(self.db_btn)
        self.layout.addWidget(self.show_info_btn)

    def change_theme(self) -> None:
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