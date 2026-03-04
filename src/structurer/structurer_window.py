import os
import sys
from pathlib import Path
import time
import traceback

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QPushButton, QTextEdit,
    QMessageBox, QProgressBar, QFileDialog, QApplication
)
from PySide6.QtCore import Signal, QThread, Slot, QSize
from PySide6.QtGui import QIcon

from src.auth.load_fonts import load_font
from src.db.database import Database
from src.structurer.structurer import Structurer

from src.interfaces import Worker, Processor

class DBWorker(Worker):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    file_processed = Signal(str, float)
    error_occurred = Signal(str, str)
    finished_all = Signal()

    def __init__(self, html_dir, login):
        super().__init__(html_dir, login)
        self.html_dir = html_dir
        self.db = Database(
            dbname="rls",
            user="postgres",
            password="postgres",
            host="localhost"
        )
        self.is_running = True
        self.login = login

    def stop_worker(self):
        self.is_running = False

    def start_worker(self):
        try:
            html_files = list(self.html_dir.glob("*.html"))
            total_files = len(html_files)

            try:
                user_id = self.db.select_user_id(self.login)
            except:
                self.error_occurred.emit("Ошибка авторизации",
                                         f"Не удалось найти пользователя {self.login} в базе данных")
                self.finished_all.emit()
                return

            for index, html_file in enumerate(html_files):
                html_file_name = str(html_file.name)
                if not self.is_running:
                    break

                try:
                    start_time = time.time()

                    self.status_updated.emit(f"Извлечение полей {html_file_name} (файл {index + 1}/{total_files})")
                    db_worker = Structurer(html_file)

                    h2_content = db_worker.structure_content('h2')
                    h3_content = db_worker.structure_content('h3')


                    for h2_header, h2_content in h2_content.items():
                        self.db.insert_second_level_content(h2_header, h2_content, html_file_name)
                        second_content_id = self.db.select_second_content_id(h2_header)
                        self.db.insert_users_second_level_content(user_id, second_content_id)

                    for h3_header, h3_content in h3_content.items():
                        self.db.insert_third_level_content(h3_header, h3_content, html_file_name)
                        third_content_id = self.db.select_third_content_id(h3_header)
                        self.db.insert_users_third_level_content(user_id, third_content_id)

                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    self.file_processed.emit(html_file_name, elapsed_time)

                except Exception as e:
                    error_details = traceback.format_exc()
                    self.error_occurred.emit(html_file_name, f"{str(e)}\n\n{error_details}")

                    continue
            self.finished_all.emit()

        except Exception as e:
            self.error_occurred.emit("Общая ошибка", traceback.format_exc())
            self.finished_all.emit()

class DBWorkWindow(Processor):
    def __init__(self, root, login):
        super().__init__()
        self.login = login
        self.worker = None
        self.setWindowTitle("Система для работы с ОХЛП")

        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.choose_lbl = QLabel("Выберите директорию со структурированными файлами ОХЛП")
        self.choose_lbl.setFont(label_font)

        self.choose_btn = QPushButton("Выбрать директорию")
        self.choose_btn.setFont(btn_font)

        self.process_btn = QPushButton("Извлечь сущности в базу данных")
        self.process_btn.setFont(btn_font)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.setFont(btn_font)
        self.cancel_btn.setEnabled(False)

        self.back_btn = QPushButton("Назад")
        self.back_btn.setFont(btn_font)
        icon = QIcon('icons/back_icon.png')
        self.back_btn.setIcon(icon)
        self.back_btn.setIconSize(QSize(30, 30))

        self.selected_dir_lbl = QLabel("Директория не выбрана")
        self.selected_dir_lbl.setWordWrap(True)
        self.selected_dir_lbl.setFont(label_font)

        self.status_lbl = QLabel("")
        self.status_lbl.setWordWrap(True)
        self.status_lbl.setFont(label_font)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setFont(label_font)

        self.current_file_lbl = QLabel("")
        self.current_file_lbl.setWordWrap(True)
        self.current_file_lbl.setVisible(False)
        self.current_file_lbl.setFont(label_font)

        self.time_lbl = QLabel("")
        self.time_lbl.setVisible(False)
        self.time_lbl.setFont(label_font)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setVisible(False)
        self.log_text.setFont(label_font)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.choose_lbl)
        self.layout.addWidget(self.choose_btn)
        self.layout.addWidget(self.process_btn)
        self.layout.addWidget(self.cancel_btn)
        self.layout.addWidget(self.selected_dir_lbl)
        self.layout.addWidget(self.status_lbl)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.current_file_lbl)
        self.layout.addWidget(self.time_lbl)
        self.layout.addWidget(self.log_text)
        self.layout.addWidget(self.back_btn)

        self.choose_btn.clicked.connect(self.choose_dir)
        self.process_btn.clicked.connect(self.process)
        self.cancel_btn.clicked.connect(self.cancel_processing)

    @Slot()
    def choose_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию с HTML-файлами",
            "",
            QFileDialog.ShowDirsOnly
        )

        if self.dir_path:
            self.selected_dir = self.dir_path
            self.selected_dir_lbl.setText(f"Выбрана директория: {self.dir_path}")

            pdf_files = self.get_files()

            if pdf_files:
                self.status_lbl.setText(f"Найдено HTML-файлов: {len(pdf_files)}")
                self.status_lbl.setStyleSheet("color: green;")
            else:
                self.status_lbl.setText("В выбранной директории нет HTML-файлов!")
                self.status_lbl.setStyleSheet("color: red;")

    @Slot()
    def cancel_processing(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop_worker()
            self.cancel_btn.setEnabled(False)
            self.status_lbl.setText("Отмена обработки...")
            self.status_lbl.setStyleSheet("color: orange;")
            self.log_message("Пользователь запросил отмену обработки")

    @Slot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    @Slot(str)
    def update_status(self, status):
        self.status_lbl.setText(status)
        self.current_file_lbl.setText(f"Текущая операция: {status}")
        self.log_message(status)

    @Slot(str, float)
    def on_file_processed(self, filename, elapsed_time):
        time_str = f"{elapsed_time:.2f} сек."
        if elapsed_time > 60:
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60
            time_str = f"{minutes} мин. {seconds:.2f} сек."

        self.time_lbl.setText(f"Последний файл: {filename} - {time_str}")
        self.log_message(f"Файл {filename} обработан за {time_str}")

    @Slot(str, str)
    def on_error(self, filename, error_details):
        error_message = f"Ошибка при обработке {filename}"
        self.status_lbl.setText(error_message)
        self.status_lbl.setStyleSheet("color: red;")
        self.log_message(f"{error_message}")
        self.log_message(f"Детали ошибки:\n{error_details}")

    @Slot()
    def on_processing_finished(self):
        self.choose_btn.setEnabled(True)
        self.process_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        if self.worker and self.worker.isRunning():
            self.worker.quit()
            self.worker.wait()

        self.progress_bar.setValue(100)
        self.status_lbl.setText("Обработка завершена!")
        self.status_lbl.setStyleSheet("color: green;")
        self.current_file_lbl.setText("Все файлы обработаны")
        self.log_message("=== ОБРАБОТКА ЗАВЕРШЕНА ===")

    def close_event(self, event):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Обработка еще не завершена. Вы уверены, что хотите выйти?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.worker.stop_worker()
                self.worker.quit()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def get_files(self):
        html_files = []
        try:
            for file in os.listdir(self.dir_path):
                if file.lower().endswith('.html'):
                    html_files.append(file)
        except Exception as e:
            self.log_message(f"Ошибка при чтении директории: {e}")

        return html_files

    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    def process(self):
        if not self.selected_dir:
            self.status_lbl.setText("Сначала выберите директорию!")
            self.status_lbl.setStyleSheet("color: red;")
            return

        html_dir = Path(self.selected_dir)
        html_files = list(html_dir.glob("*.html"))

        if not html_files:
            self.status_lbl.setText("В выбранной директории нет PDF-файлов!")
            self.status_lbl.setStyleSheet("color: red;")
            return

        self.log_text.clear()
        self.log_text.setVisible(True)

        self.worker = Worker(html_dir, self.login)

        self.worker.progress_updated.connect(self.update_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.file_processed.connect(self.on_file_processed)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished_all.connect(self.on_processing_finished)

        self.log_message("Начало обработки...")
        self.log_message(f"Найдено файлов для обработки: {len(html_files)}")
        self.worker.start_worker()

# if __name__ == "__main__":
#     app = QApplication([])
#
#     current_file = Path(__file__).resolve()
#     root = current_file.parents[1]
#
#     widget = DBWorkWindow(root, "test")
#
#     with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
#         style_sheet = f.read()
#         widget.setStyleSheet(style_sheet)
#
#     widget.resize(700, 300)
#     widget.show()
#
#     sys.exit(app.exec())