from bs4 import BeautifulSoup

html_path = r"C:\Users\khach\OneDrive\Desktop\input\HTML\Фирмагон\Фирмагон.html"

with open(html_path, "r", encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

h2_headers = soup.find_all('h2')
h3_headers = soup.find_all('h3')

for h2_header in h2_headers:
    print(h2_header.text)

    next_p = h2_header.find_next('p')
    if next_p:
        print(next_p.text)
    else:
        print("Нет p после заголовка")

# for h3_header in h3_headers:
#     print(h3_header.text)
#
#     next_p = h3_header.find_next('p')
#     if next_p:
#         print(next_p.text)
#     else:
#         print("Нет p после заголовка")