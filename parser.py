import requests
from bs4 import BeautifulSoup

def parse_news(limit=5, language=None):
    url = "https://pythondigest.ru/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    news_data = []
    news_items = soup.find_all("div", class_="issue-item")

    for item in news_items[:limit]:
        title = item.find("a", class_="issue-item-title").get_text(strip=True)
        description_tag = item.find("p", class_="issue-item-description")
        description = description_tag.get_text(strip=True) if description_tag else ""
        link = item.find("a", class_="issue-item-title")["href"]
        
        # Добавляем фильтрацию по языку, если указано
        if language:
            badge = item.find("span", class_="issue-item-language")
            if badge and badge.get("title") != language:
                continue

        news_data.append({
            "title": title,
            "description": description,
            "link": link
        })

    return news_data
