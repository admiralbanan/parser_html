from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Базовый класс для моделей данных
Base = declarative_base()

# Определение модели News
class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    link = Column(String, nullable=False)
    parsed_date = Column(Date, default=datetime.utcnow)

# Создаем движок базы данных SQLite
engine = create_engine('sqlite:///news.db', echo=True)
Session = sessionmaker(bind=engine)
