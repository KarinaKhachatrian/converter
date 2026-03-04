from pathlib import Path
from bs4 import BeautifulSoup


class Structurer:
    def __init__(self, html_path: Path):
        self.html_path = html_path

    @staticmethod
    def clean_headers(soup: BeautifulSoup, tag_name: str) -> BeautifulSoup:
        headers = soup.find_all(tag_name)

        for header in headers:
            if header.parent.name == 'p':
                header.parent.unwrap()

        return soup


    def structure_content(self, tag_name: str) -> dict:
        with open(self.html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        soup = self.clean_headers(soup, tag_name)

        headers = soup.find_all(tag_name)
        content = {}

        for i, h in enumerate(headers):
            h_text = h.get_text(strip=True)
            p_content = []

            next_elements = h.find_next_siblings()

            for el in next_elements:
                if el.name == tag_name:
                    break

                if el.name == 'p':
                    p_content.append(el.get_text(strip=True))

            content[h_text] = '\n'.join(p_content)

        return content