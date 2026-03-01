from bs4 import BeautifulSoup, Tag
from src.db.database import Database
from clean_headers import clean_headers

db = Database(
    dbname="rls",
    user="postgres",
    password="postgres",
    host="localhost"
)


def structure_content(html_path: str, tag_name: str) -> dict:
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    soup = clean_headers(soup, tag_name)

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

html_path = r"C:\Users\khach\OneDrive\Desktop\input\HTML\Фирмагон\Фирмагон.html"

h2_content = structure_content(html_path, 'h2')
h3_content = structure_content(html_path, 'h3')

for h2_header, h2_content in h2_content.items():
    db.insert_second_level_content(h2_header, h2_content)

for h3_header, h3_content in h3_content.items():
    db.insert_third_level_content(h3_header, h3_content)