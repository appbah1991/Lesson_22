from flask import Flask, render_template, request
from main import parsing_news, data_base_add, data_base_search_data

app = Flask(__name__)

@app.route("/")
def index():

    return render_template('index.html')


@app.route('/contacts/')
def contacts():
    developer_name = 'Baha'

    return render_template('contacts.html', name=developer_name, creation_date='02.07.2022')


@app.route('/form/', methods=['GET'])
def run_get():

    return render_template('form.html')

@app.route('/news_search/', methods=['GET'])
def run_get_search():

    return render_template('news_search.html')

@app.route('/news_search/', methods=['POST'])
def run_post_search():
    # Берем запрос из формы
    text = request.form['input_text_news']
    # Выполняем поиск по названиям статей из базы
    data_base_search_data(text)
    # Открываем файл с результатми запроса и сохраняем данные из него в переменную, которую выведем на результирующей странице

    with open("search_result.txt", "r", encoding='utf8') as file:
        text_of_search = file.read()

    return render_template('news_search_result.html', text_of_search=text_of_search)


@app.route('/form/', methods=['POST'])
def run_post():
    text = request.form['input_text']
    dict_of_news = parsing_news(text)
    data_base_add(name_of_db='news.sqlite', dict = dict_of_news)
    with open('main.txt', 'a', encoding='utf8') as f:
        f.write(f'{dict_of_news}\n')
    return render_template('good.html')




@app.route('/results/')
def results():
    data = open('main.txt', 'r', encoding='utf8')
    return render_template('results.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)