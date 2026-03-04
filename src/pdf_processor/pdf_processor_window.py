import sys
import os
from pathlib import Path
import shutil
import time
import traceback

from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
    QPushButton, QTextEdit,
    QMessageBox, QProgressBar, QFileDialog, QApplication
)
from PySide6.QtCore import Signal, QThread, Slot, QSize
from PySide6.QtGui import QIcon

from src.pdf_processor.pdf_converter import PDFConverter
from src.pdf_processor.stamps_extractor import StampsExtractor
from src.pdf_processor.images_converter import ImagesConverter
from src.pdf_processor.ocr import OCRProcessor
from src.pdf_processor.document_processor import DocumentProcessor
from src.pdf_processor.html_converter import HTMLConverter
from src.pdf_processor.html_processor import HTMLProcessor
from src.pdf_processor.tables_fixer import TablesFixer
from src.pdf_processor.wrapper import Wrapper

from src.auth.load_fonts import load_font


class Worker(QThread):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    file_processed = Signal(str, float)
    error_occurred = Signal(str, str)
    finished_all = Signal()

    def __init__(self, pdf_dir):
        super().__init__()
        self.pdf_dir = pdf_dir
        self.is_running = True

    def stop(self):
        """Остановка обработки"""
        self.is_running = False

    def run(self):
        try:
            pdf_files = list(self.pdf_dir.glob("*.pdf"))
            total_files = len(pdf_files)

            for index, pdf_file in enumerate(pdf_files):
                if not self.is_running:
                    break

                try:
                    start_time = time.time()

                    images_dir = self.pdf_dir / f'{pdf_file.stem}_images'
                    processed_images_dir = self.pdf_dir / f'{pdf_file.stem}_processed_images'
                    processed_pdf_dir = self.pdf_dir / f'{pdf_file.stem}_processed'
                    docx_dir = self.pdf_dir / 'docx'
                    certain_html_dir = self.pdf_dir / 'HTML' / pdf_file.stem

                    os.makedirs(images_dir, exist_ok=True)
                    os.makedirs(processed_images_dir, exist_ok=True)
                    os.makedirs(processed_pdf_dir, exist_ok=True)
                    os.makedirs(docx_dir, exist_ok=True)
                    os.makedirs(certain_html_dir, exist_ok=True)

                    processed_pdf_path = processed_pdf_dir / Path(f'{pdf_file.stem}.pdf')
                    docx_path = docx_dir / Path(f'{processed_pdf_path.stem}.docx')
                    html_path = certain_html_dir / Path(f'{pdf_file.stem}.html')

                    self.status_updated.emit(f"Обработка {pdf_file.name} (файл {index + 1}/{total_files})")

                    self.status_updated.emit(f"Конвертация PDF в изображения: {pdf_file.name}")
                    pdf_converter = PDFConverter(pdf_file, images_dir, workers=8)
                    pdf_converter.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Обработка изображений: {pdf_file.name}")
                    extractor = StampsExtractor(images_dir, processed_images_dir, workers=8)
                    extractor.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Создание PDF: {pdf_file.name}")
                    images_converter = ImagesConverter(processed_images_dir, processed_pdf_path)
                    images_converter.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Распознавание текста: {pdf_file.name}")
                    ocr_processor = OCRProcessor(processed_pdf_path, docx_dir)
                    ocr_processor.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Обработка документа: {pdf_file.name}")
                    document_processor = DocumentProcessor(str(docx_path))
                    document_processor.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Конвертация в HTML: {pdf_file.name}")
                    html_converter = HTMLConverter(docx_path, html_path)
                    html_converter.process()

                    if not self.is_running:
                        break

                    self.status_updated.emit(f"Оптимизация HTML: {pdf_file.name}")
                    html_processor = HTMLProcessor(html_path)
                    html_processor.process()

                    TablesFixer.finalize(html_path)
                    Wrapper.finalize(html_path)

                    end_time = time.time()
                    elapsed_time = end_time - start_time

                    shutil.rmtree(images_dir, ignore_errors=True)
                    shutil.rmtree(processed_images_dir, ignore_errors=True)
                    shutil.rmtree(processed_pdf_dir, ignore_errors=True)
                    shutil.rmtree(docx_dir, ignore_errors=True)

                    self.file_processed.emit(pdf_file.name, elapsed_time)

                    progress_value = int((index + 1) / total_files * 100)
                    self.progress_updated.emit(progress_value)

                except Exception as e:
                    error_details = traceback.format_exc()
                    self.error_occurred.emit(pdf_file.name, f"{str(e)}\n\n{error_details}")

                    continue

            self.finished_all.emit()

        except Exception as e:
            self.error_occurred.emit("Общая ошибка", traceback.format_exc())
            self.finished_all.emit()


class ProcessorWindow(QWidget):
    def __init__(self, root):
        super().__init__()
        self.setWindowTitle("PDF Конвертер")

        self.selected_dir = None
        self.worker = None

        
        label_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Medium.ttf')
        label_font = load_font(label_font_path, 13)

        btn_font_path = str(root / r'fonts/Montserrat/static/Montserrat-Black.ttf')
        btn_font = load_font(btn_font_path, 13)

        self.choose_lbl = QLabel("Выберите директорию с PDF-файлами ОХЛП")
        self.choose_lbl.setFont(label_font)
        
        self.choose_btn = QPushButton("Выбрать директорию")
        self.choose_btn.setFont(btn_font)
        
        self.process_btn = QPushButton("Конвертировать файлы")
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
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию с PDF-файлами",
            "",
            QFileDialog.ShowDirsOnly
        )

        if dir_path:
            self.selected_dir = dir_path
            self.selected_dir_lbl.setText(f"Выбрана директория: {dir_path}")

            pdf_files = self.get_pdf_files(dir_path)

            if pdf_files:
                self.status_lbl.setText(f"Найдено PDF-файлов: {len(pdf_files)}")
                self.status_lbl.setStyleSheet("color: green;")
            else:
                self.status_lbl.setText("В выбранной директории нет PDF-файлов!")
                self.status_lbl.setStyleSheet("color: red;")

    def get_pdf_files(self, dir_path):
        pdf_files = []
        try:
            for file in os.listdir(dir_path):
                if file.lower().endswith('.pdf'):
                    pdf_files.append(file)
        except Exception as e:
            self.log_message(f"Ошибка при чтении директории: {e}")

        return pdf_files

    def log_message(self, message):
        """Добавление сообщения в лог"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")

        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

    @Slot()
    def process(self):
        if not self.selected_dir:
            self.status_lbl.setText("Сначала выберите директорию!")
            self.status_lbl.setStyleSheet("color: red;")
            return

        pdf_dir = Path(self.selected_dir)
        pdf_files = list(pdf_dir.glob("*.pdf"))

        if not pdf_files:
            self.status_lbl.setText("В выбранной директории нет PDF-файлов!")
            self.status_lbl.setStyleSheet("color: red;")
            return

        self.log_text.clear()
        self.log_text.setVisible(True)

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.current_file_lbl.setVisible(True)
        self.time_lbl.setVisible(True)

        self.choose_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.worker = Worker(pdf_dir)

        self.worker.progress_updated.connect(self.update_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.file_processed.connect(self.on_file_processed)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished_all.connect(self.on_processing_finished)

        self.log_message("Начало обработки...")
        self.log_message(f"Найдено файлов для обработки: {len(pdf_files)}")
        self.worker.start()

    @Slot()
    def cancel_processing(self):
        """Отмена обработки"""
        if self.worker and self.worker.isRunning():
            self.worker.stop_worker()
            self.cancel_btn.setEnabled(False)
            self.status_lbl.setText("Отмена обработки...")
            self.status_lbl.setStyleSheet("color: orange;")
            self.log_message("Пользователь запросил отмену обработки")

    @Slot(int)
    def update_progress(self, value):
        """Обновление прогресс-бара"""
        self.progress_bar.setValue(value)

    @Slot(str)
    def update_status(self, status):
        """Обновление статуса"""
        self.status_lbl.setText(status)
        self.current_file_lbl.setText(f"Текущая операция: {status}")
        self.log_message(status)

    @Slot(str, float)
    def on_file_processed(self, filename, elapsed_time):
        """Обработка успешно завершенного файла"""
        time_str = f"{elapsed_time:.2f} сек."
        if elapsed_time > 60:
            minutes = int(elapsed_time // 60)
            seconds = elapsed_time % 60
            time_str = f"{minutes} мин. {seconds:.2f} сек."

        self.time_lbl.setText(f"Последний файл: {filename} - {time_str}")
        self.log_message(f"Файл {filename} обработан за {time_str}")

    @Slot(str, str)
    def on_error(self, filename, error_details):
        """Обработка ошибок"""
        error_message = f"Ошибка при обработке {filename}"
        self.status_lbl.setText(error_message)
        self.status_lbl.setStyleSheet("color: red;")
        self.log_message(f"{error_message}")
        self.log_message(f"Детали ошибки:\n{error_details}")

    @Slot()
    def on_processing_finished(self):
        """Завершение обработки"""
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

    def closeEvent(self, event):
        """Обработка закрытия окна"""
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


# if __name__ == "__main__":
#     app = QApplication([])
#
#     current_file = Path(__file__).resolve()
#     root = current_file.parents[1]
#
#     widget = ProcessorWindow(root)
#
#     with open(root / r"styles/light.qss", "r", encoding="utf-8") as f:
#         style_sheet = f.read()
#         widget.setStyleSheet(style_sheet)
#
#     widget.resize(700, 300)
#     widget.show()
#
#     sys.exit(app.exec())