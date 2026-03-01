from bs4 import BeautifulSoup

def clean_headers(soup: BeautifulSoup, tag_name: str) -> BeautifulSoup:
    headers = soup.find_all(tag_name)

    for header in headers:
        if header.parent.name == 'p':
            header.parent.unwrap()

    return soup