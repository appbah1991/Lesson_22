# Импортируем библиотеки
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pickle

def parsing_news(req_user):

    # Поисковый запрос - рекомендую 'java', тк там не очень много страниц.
    # По запросу 'python' их 289 - поэтому прога будет долго работать
    req = str(req_user).replace(' ', '+')

    # Определяем нужные переменные - список словарей всех новостей и номер страницы, которую будем парсить
    dict_of_news_all = []
    num_of_page = 1

    # Ссылка на сайт, который будем парсить с переменной запроса
    url = f'https://pythondigest.ru/feed/?q={req}'

    # Делаем запрос на сайт
    responce = requests.get(url)

    # Цикл - работает пока ответ от сайта не будет 404. Перебираем страницы по запросу.
    # То есть пока есть новая страница мы парсим, как только страницы заканчиваются - цикл тоже заканчивается
    while str(responce) != '<Response [404]>':

        # Новый урл уже с номером страницы для цикла
        url = f'https://pythondigest.ru/feed/?q={req}&page={num_of_page}'

        # запрос на урл, так же, создаем объект класса бьютифул суп
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')

        # список всех блоков новостей с вложенными тегами
        list_of_find_one_page = soup.find_all('div', class_="news-line-item")

        # цикл для перебора новостей на 1 странице
        for item in list_of_find_one_page:

            # вытаскиваем ссылку из объекта тега а
            url_one_news = item.a['href']

            # вытаскиваем заголовок новости
            soup_header = item.a.get_text()

            # вытаскиваем всю новость с заголовком
            block_of_news = item.get_text()

            # отрезаем заголовок
            block_of_news = str(block_of_news).replace(soup_header, '')

            # добавляем полученные данные в словарь
            dict_of_news = {
                'header': soup_header,
                'url': url_one_news,
                'news': block_of_news
            }

            # добавляем получившийся словарь в список новостей
            dict_of_news_all.append(dict_of_news)

        # принтим прогресс
        print(f'Страница {num_of_page} пройдена...')

        # добавляем +1 к счетчику страниц
        num_of_page += 1
    return dict_of_news_all



def data_base_add(name_of_db, dict):
    conn = sqlite3.connect(name_of_db)

    cursor = conn.cursor()

    for news in dict:
        one_news_title = news['header']
        one_news_url = news['url']
        one_news_news = news['news']
        cursor.execute("insert into table_of_news (title, url, news) VALUES (?, ?, ?)", (one_news_title, one_news_url, one_news_news))
        conn.commit()


def data_base_search_data(text_search):
# Удаляем предыдущий файл с результатами поиска
    if os.path.isfile('search_result.txt'):
        os.remove('search_result.txt')
# Подключаемся к базе
    conn = sqlite3.connect('news.sqlite')
# Создаем курсор
    cursor = conn.cursor()
# Пишем текст запроса
    query = 'select news, title from table_of_news'
# Выполняем запрос
    cursor.execute(query)
# Сохраняем все результаты запроса в переменную
    data_from_base = cursor.fetchall()
# Определяем текст поиска для цикла
    text_search = text_search
# Задаем счетчик цикла
    index = 0
# Сам цикл - ищем по данным в таблице, перебирая кортежи (заголовок, новость)
    for item in data_from_base:
        # если текст поиска соответствует заголовку
        if text_search.lower() in data_from_base[index][1].lower():
            # открываем файл и пишем в него заголовок и саму новость
            with open('search_result.txt', 'a', encoding='utf8') as f:
                f.write(f'"{item[1]}"\n"{item[0]}"\n\n')
# Увеличиваем счетчик на 1
        index += 1



engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    title = Column(String)


    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'{self.title}'

class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __init__(self, url):
        self.url = url
    def __str__(self):
        return f'{self.url}'

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    news = Column(String)

    def __init__(self, news):
        self.news = news
    def __str__(self):
        return f'{self.news}'


def data_base_add_classes(dict):

    for news in dict:
        one_news_title = Title(news['header'])

        one_news_url = Url(news['url'])

        one_news_news = News(news['news'])

        with open('main.txt', 'a', encoding='utf8') as f:
            f.write(f'{one_news_title}\n{one_news_url}\n{one_news_news}\n\n')




