import csv
import os
from typing import Optional

import requests
from bs4 import BeautifulSoup


def _get_html(url: str) -> Optional[str]:
    """
    Take url address and returns response's content in Unicode
    :param url: url address: string
    :return: string if url available or None otherwise
    """
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        return r.text
    except:
        return None


def _write_csv(data: dict) -> None:
    """
    Write data from dictionary into the file habr_top.csv
    :param data: information about article
    :return: None
    """
    if not os.path.isfile('./habr_top.csv'):
        with open('habr_top.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(
                ('Заголовок поста',
                 'Имя автора поста',
                 'Дата публикации',
                 'Краткое описание поста')
            )
    with open('habr_top.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(
            (data['title'],
            data['author'],
            data['pub_date'],
            data['text'])
        )


def _get_one_page_data(number: 'int, 0 < number <= 20', url: str) -> None:
    """
    Put information about articles from any html page into dictionary and then write into the file
    :param number: integer, 0 < int <= 20
    :param url: url address of html page, string
    :return: None
    """
    counter = 1
    html = _get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('article', class_="post post_preview")

    for article in articles:
        if counter > number or counter > 20:
            break
        title = article.find('h2', class_='post__title').text
        author = article.find('span', class_='user-info__nickname user-info__nickname_small').text
        pub_date = article.find('span', class_='post__time').text
        text = article.find('div', class_='post__text post__text-html js-mediator-article').text
        data = {
            'title': title,
            'author': author,
            'pub_date': pub_date,
            'text': text
        }
        _write_csv(data)
        counter += 1


def get_habr_top(number: 'int, number < 1001') -> None:
    """
    Get number of articles and write into the file habr_top.csv information about these articles
    :param number: number of articles to be displayed
    :return: None
    """
    url_start = 'https://habr.com/ru/top/yearly/page'

    if number <= 20:
        _get_one_page_data(number, 'https://habr.com/ru/top/yearly/')
    elif number < 1001:
        _get_one_page_data(20, 'https://habr.com/ru/top/yearly/')
        full_pages = number // 20
        rest_aticles = number % 20
        for i in range(2, full_pages+1):
            url = url_start + str(i) + '/'
            _get_one_page_data(20, url)
        if rest_aticles > 0:
            url = url_start + str(full_pages+1) + '/'
            _get_one_page_data(rest_aticles, url)
    else:
        get_habr_top(1000)
