import os
import subprocess
from pathlib import Path

from src.pdf_processor.processor import Processor


class HTMLConverter(Processor):
    def __init__(self, docx_path: Path, html_path: Path):
        self.docx_path = docx_path
        self.html_path = html_path
        self.html_dir = html_path.parent
        self.html_header = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        table {
            table-layout: fixed;
            width: 100%;
            border-collapse: collapse;
            border: 1px solid black;
        }
        td {
              vertical-align: middle;
              word-wrap: break-word;
        }
        th, td {
            width: 25%;
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            vertical-align: top;
            overflow-wrap: break-word;
            word-break: break-word;
        }
    </style>
</head>
<body>
    """
        self.html_footer = """
    </body>
</html>
"""
        if not os.path.exists(self.html_dir):
            os.makedirs(self.html_dir, exist_ok=True)

    @staticmethod
    def read_content(filepath: Path) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    @staticmethod
    def write_content(filepath: Path, content: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def process(self):
        cmd = [
            'pandoc',
            os.path.abspath(self.docx_path),
            '-f', 'docx',
            '-t', 'html',
            '--number-sections=false',
            f'--extract-media={self.html_dir}',
            '-o', os.path.abspath(self.html_path),
        ]

        try:
            subprocess.run(cmd, check=True)

            html_content = self.read_content(self.html_path)
            self.write_content(self.html_path,
                               self.html_header
                               + html_content
                               + self.html_footer)

        except FileNotFoundError:
            print("Ошибка: pandoc не найден. Убедитесь, что pandoc установлен и добавлен в PATH.")
        except Exception as e:
            print(f'Произошла ошибка: {e}')
