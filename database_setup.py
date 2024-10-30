from models import Base, engine

# Создаем все таблицы, описанные в моделях
Base.metadata.create_all(engine)
