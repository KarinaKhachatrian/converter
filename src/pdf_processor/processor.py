from pathlib import Path

from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def process(self) -> None:
        """Запуск процесса обработки файлов"""

    @classmethod
    def finalize(cls, html_path: Path, parser='html.parser') -> None:
        """Доработка html-разметки"""

    @staticmethod
    def read_content(filepath: Path) -> str:
        """Чтение файла построчно"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    @staticmethod
    def read_lines(filepath: Path) -> list:
        """Чтение файла полинейно"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    @staticmethod
    def write_content(filepath: Path, content: str) -> None:
        """Запись строчного содержимого"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def write_binary(filepath: Path, content: bytes):
        """Запись бинарного содержимого"""
        with open(filepath, 'wb') as f:
            f.write(content)
