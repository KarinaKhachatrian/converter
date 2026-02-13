from pathlib import Path
from bs4 import BeautifulSoup

from src.pdf_processor.headers import h2_headers, h3_headers
from src.pdf_processor.processor import Processor

class HTMLProcessor(Processor):
    def __init__(self, html_path: Path):
        self.html_path = html_path

    @staticmethod
    def write_content(filepath: Path, content: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def fix_images(soup: BeautifulSoup) -> None:
        for img in soup.find_all('img'):
            src = '/'.join(img['src'].split('/')[1:])
            img['src'] = src

    @staticmethod
    def unwrap_elements(elements) -> None:
        for element in elements:
            element.unwrap()

    @staticmethod
    def apply_headers(soup: BeautifulSoup) -> None:
        for strong in soup.find_all('strong'):
            text = strong.text.replace('\n', ' ')
            processed_text = text.split('.')

            if len(processed_text) >= 2:
                if processed_text[0].isdigit():
                    h2_check = any(processed_text[1].lstrip().startswith(h2) for h2 in h2_headers)
                    if h2_check:
                        h2_tag = soup.new_tag('h2')
                        h2_tag.string = text
                        strong.replace_with(h2_tag)

                if processed_text[0].isdigit() and processed_text[1].isdigit():
                    h3_key = None
                    for h3_header in h3_headers.keys():
                        if processed_text[2].strip().startswith(h3_header):
                            h3_key = h3_header
                            break
                    if h3_key:
                        h3_tag = soup.new_tag('h3')
                        h3_tag.string = text
                        strong.replace_with(h3_tag)

    @staticmethod
    def clean_pages(soup: BeautifulSoup) -> None:
        p_tags = soup.find_all('p')
        for p in p_tags:
            text = p.text.strip()
            if text.startswith('С.') or text.startswith('Стр.') or text.startswith('Страница'):
                p.extract()

    def process(self):
        with open(self.html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        unwrap_elements = soup.find_all(['blockquote', 'colgroup', 'col'])
        self.unwrap_elements(unwrap_elements)
        self.write_content(self.html_path, soup.prettify())

        self.fix_images(soup)
        self.apply_headers(soup)
        self.clean_pages(soup)
        self.write_content(self.html_path, soup.prettify())

