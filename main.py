# Импортируем библиотеки
import requests
from bs4 import BeautifulSoup

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



