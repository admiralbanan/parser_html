from flask import Flask, render_template, request, redirect, url_for
from models import Session, News
from parser import parse_news
from datetime import datetime

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template("index.html", title="Главная страница")

# Страница для всех новостей
@app.route('/news')
def news():
    session = Session()
    news_data = session.query(News).all()
    session.close()
    return render_template("news.html", title="Новости", news=news_data)

# Страница поиска новостей
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        limit = int(request.form.get("limit", 5))
        news_data = parse_news(limit=limit)

        # Сохраняем данные в базу, если данные получены
        session = Session()
        for news in news_data:
            news_entry = News(
                title=news['title'],
                description=news['description'],
                link=news['link'],
                parsed_date=datetime.utcnow()
            )
            session.add(news_entry)
        session.commit()
        session.close()

        # Отправляем данные на страницу с результатами
        return render_template("results.html", title="Результаты поиска", news=news_data)

    return render_template("form.html", title="Форма поиска")

# Страница контактов
@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакты")

# Запуск приложения Flask
if __name__ == "__main__":
    app.run(debug=True)
