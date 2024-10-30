from flask import Flask, render_template, request, redirect, url_for
from parser import parse_news
from cache import Cache

app = Flask(__name__)
cache = Cache()

# Главная страница
@app.route('/')
def index():
    title = "Главная страница"
    return render_template("index.html", title=title)

# Страница контактов
@app.route('/contacts')
def contacts():
    title = "Контакты"
    contact_info = {"email": "info@example.com", "phone": "+1 (123) 456-7890"}
    return render_template("contacts.html", title=title, contact_info=contact_info)

# Страница с формой для поиска
@app.route('/form', methods=["GET", "POST"])
def form():
    title = "Форма поиска"
    if request.method == "POST":
        query = request.form.get("query")
        limit = int(request.form.get("limit", 5))
        
        # Проверяем кэш перед запуском парсера
        cache_key = f"{query}_{limit}"
        cached_result = cache.load(cache_key)
        
        if cached_result:
            return render_template("results.html", title="Результаты", results=cached_result)
        
        # Запускаем парсер, если результата в кэше нет
        results = parse_news(limit=limit)
        cache.save(cache_key, results)
        return render_template("results.html", title="Результаты", results=results)
    
    return render_template("form.html", title=title)

if __name__ == "__main__":
    app.run(debug=True)
