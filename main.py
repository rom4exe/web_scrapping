import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


headers_gen = Headers(os="win", browser="chrome")
response = requests.get('https://habr.com/ru/articles/', headers=headers_gen.generate())
html_data = response.text
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

soup = BeautifulSoup(html_data, 'lxml')
articles_list = soup.find('div', class_="tm-articles-list")
articles_tags = articles_list.find_all("article")

for article_tag in articles_tags:
    header_tag = article_tag.find("h2")
    a_tag = header_tag.find("a")
    time_tag = article_tag.find("time")

    header = header_tag.text
    link_relative = a_tag["href"]
    link_absolute = f"https://habr.com{link_relative}"
    publish_time = time_tag["datetime"]

    article_full_html = requests.get(link_absolute, headers=headers_gen.generate()).text
    article_full_soup = BeautifulSoup(article_full_html, "lxml")

    article_full_tag = article_full_soup.find("div", attrs={"id": "post-content-body"})
    article_full_text = article_full_tag.text

    for search_word in KEYWORDS:
        if search_word.lower() in header.lower() or search_word.lower() in article_full_text.lower():
            print(f'Дата: {publish_time} - Заголовок: {header} - Ссылка: {link_absolute}')

