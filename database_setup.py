import sqlite3

# Подключаемся к базе данных и создаем таблицу
conn = sqlite3.connect('news.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        link TEXT NOT NULL,
        parsed_date DATE DEFAULT CURRENT_DATE
    )
''')

conn.commit()
conn.close()
