from flask import Flask, render_template, request
import sqlite3
from parser import parse_news

app = Flask(__name__)

# Функция для подключения к базе данных и выполнения SQL-запросов
def connect_db():
    return sqlite3.connect('news.db', check_same_thread=False)

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template("index.html", title="Главная страница")

# Маршрут для страницы контактов
@app.route('/contacts')
def contacts():
    contact_info = {"email": "info@example.com", "phone": "+1 (123) 456-7890"}
    return render_template("contacts.html", title="Контакты", contact_info=contact_info)

# Маршрут для формы поиска и сохранения данных в базе
@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        limit = int(request.form.get("limit", 5))
        news_data = parse_news(limit=limit)

        conn = connect_db()
        cursor = conn.cursor()
        for news in news_data:
            cursor.execute('''
                INSERT INTO news (title, description, link)
                VALUES (?, ?, ?)
            ''', (news['title'], news['description'], news['link']))
        conn.commit()
        conn.close()

        return render_template("news.html", title="Результаты поиска", news=news_data)
    
    return render_template("form.html", title="Форма поиска")

# Маршрут для отображения всех новостей из базы данных
@app.route('/news')
def news():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM news')
    news_data = cursor.fetchall()
    conn.close()
    return render_template("news.html", title="Новости", news=news_data)

if __name__ == "__main__":
    app.run(debug=True)
