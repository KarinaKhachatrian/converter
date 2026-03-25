from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QThread, Slot, Signal

class Worker(QThread):
    """Инициализация сигналов"""
    progress_updated = Signal(int)
    status_updated = Signal(str)
    file_processed = Signal(str, float)
    error_occurred = Signal(str, str)

    def __init__(self, dir, login):
        super().__init__()
        self.dir = dir
        self.login = login

    finished_all = Signal()
    def stop_worker(self):
        """Остановка обработки"""

    def start_worker(self):
        """Запуск обработки"""

class Processor(QWidget):
    @Slot()
    def choose_dir(self):
        """Выбор директории"""

    @Slot()
    def cancel_processing(self):
        """Отмена обработки"""

    @Slot(int)
    def update_progress(self, value):
        """Обновление прогресс-бара"""

    @Slot(str)
    def update_status(self, status):
        """Обновление статуса"""

    @Slot(str, float)
    def file_processed(self, filename, elapsed_time):
        """Обработка успешно завершенного файла"""

    @Slot(str, str)
    def error(self, filename, error_details):
        """Обработка ошибок"""

    @Slot()
    def processing_finished(self):
        """Завершение обработки"""

    def get_files(self):
        """Чтение файлов"""

    def log_message(self, message):
        """Добавление сообщения в лог"""

    def process(self):
        """Запуск процесса обработки"""

    def close_event(self, event):
        """Обработка закрытия окна"""