from flask import Flask, render_template, request
from main import parsing_news

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
    # with open('main.txt', 'r', encoding='utf8') as f:     #здесь можно раскоментить и выводить данные прямо на странице запроса
    #     text = f.read()
    return render_template('form.html')



@app.route('/form/', methods=['POST'])
def run_post():
    text = request.form['input_text']
    dict_of_news = parsing_news(text)
    with open('main.txt', 'a', encoding='utf8') as f:
        f.write(f'{dict_of_news}\n')
    return render_template('good.html')


@app.route('/results/')
def results():
    data = open('main.txt', 'r', encoding='utf8')
    return render_template('results.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)