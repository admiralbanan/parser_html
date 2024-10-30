import requests
from bs4 import BeautifulSoup
import csv

# URL страницы Python Digest
url = "https://pythondigest.ru/"

# Отправка запроса на страницу
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Список для хранения новостей
news_data = []

# Поиск элементов с новостями
news_items = soup.find_all("div", class_="issue-item")

for item in news_items:
    title = item.find("a", class_="issue-item-title").get_text(strip=True)
    description_tag = item.find("p", class_="issue-item-description")
    description = description_tag.get_text(strip=True) if description_tag else ""
    link = item.find("a", class_="issue-item-title")["href"]

    # Добавление данных в список
    news_data.append([title, description, link])

# Сохранение в CSV
with open("python_digest_news.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Description", "Link"])
    writer.writerows(news_data)

print("Данные успешно сохранены в файл python_digest_news.csv")
