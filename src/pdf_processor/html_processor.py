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
            text = strong.get_text(strip=True).replace('\n', ' ')

            if len(text) >= 2:
                if text[0].isdigit():
                    h2_check = any(h2 in text for h2 in h2_headers)
                    h3_check = any(h3 in text for h3 in h3_headers)

                    if h2_check:
                        print(text)
                        h2_tag = soup.new_tag('h2')
                        h2_tag.string = text
                        strong.replace_with(h2_tag)

                    elif h3_check:
                        h3_tag = soup.new_tag('h3')
                        h3_tag.string = text
                        strong.replace_with(h3_tag)

    @staticmethod
    def clean_headers(soup: BeautifulSoup, tag_name: str) -> None:
        headers = soup.find_all(tag_name)

        for header in headers:
            if header.parent.name == 'p':
                header.parent.unwrap()

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
        self.clean_headers(soup, 'h2')
        self.clean_headers(soup, 'h3')
        self.clean_pages(soup)
        self.write_content(self.html_path, soup.prettify())

