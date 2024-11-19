from models import News, Session
from parser import parse_news
from datetime import datetime

# Функция для добавления новостей в базу данных
def add_news_to_db(news_list):
    session = Session()
    for news in news_list:
        news_entry = News(
            title=news['title'],
            description=news['description'],
            link=news['link'],
            parsed_date=datetime.utcnow()
        )
        session.add(news_entry)
    session.commit()
    session.close()
    print("Данные добавлены в базу.")

# Функция для выборки данных из базы
def fetch_news_from_db():
    session = Session()
    news_list = session.query(News).all()
    session.close()
    return news_list

# Получаем данные через парсер и добавляем их в базу данных
news_data = parse_news(limit=5)
add_news_to_db(news_data)

# Выполняем выборку и отображаем данные
fetched_news = fetch_news_from_db()
for news in fetched_news:
    print(f"ID: {news.id}, Title: {news.title}, Link: {news.link}, Date: {news.parsed_date}")
