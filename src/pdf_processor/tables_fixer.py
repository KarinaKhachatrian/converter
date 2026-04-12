from pathlib import Path
from bs4 import BeautifulSoup

from src.pdf_processor.processor import Processor


class TablesFixer(Processor):
    @staticmethod
    def read_lines(filepath: Path) -> list:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines

    @staticmethod
    def write_content(filepath: Path, content: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @classmethod
    def finalize(cls, html_path: Path, parser='html.parser'):
        lines = cls.read_lines(html_path)

        for i in range(len(lines) - 1):
            if lines[i].strip().startswith("</table") and lines[i + 1].strip().startswith("<table"):
                lines[i], lines[i + 1] = '', ''

        content = ''.join(lines)
        soup = BeautifulSoup(content, parser).prettify()
        cls.write_content(html_path, soup)

        content = cls.read_content(html_path)
        soup = BeautifulSoup(content, parser)
        tables = soup.find_all('table')
        for table in tables:
            tbodies = table.find_all('tbody')
            if len(tbodies) > 1:
                for tbody in tbodies:
                    tbody.unwrap()

        cls.write_content(html_path, soup.prettify())

