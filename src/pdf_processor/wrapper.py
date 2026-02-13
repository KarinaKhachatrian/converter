from bs4 import BeautifulSoup
from pathlib import Path

from src.pdf_processor.processor import Processor

class Wrapper(Processor):
    @staticmethod
    def read_content(filepath: Path) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

    @staticmethod
    def write_content(filepath: Path, content: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    @classmethod
    def finalize(cls, html_path: Path, parser='html.parser') -> None:
        content = cls.read_content(html_path)
        soup = BeautifulSoup(content, parser)

        for p in soup.find_all("p"):
            children = [c for c in p.contents if not (str(c).isspace())]

            if children and all(c.name == "img" for c in children):
                div = soup.new_tag("div")
                for child in children:
                    div.append(child)
                p.replace_with(div)

        for table in soup.find_all("table"):
            parent = table.parent
            if not (parent.name == "div" and "table-responsive" in parent.get("class", [])):
                wrapper = soup.new_tag("div", **{"class": "table-responsive"})
                table.replace_with(wrapper)
                wrapper.append(table)

        cls.write_content(html_path, soup.prettify())

