"""
Миграция для добавления начальных тарифов
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Tariff

def init_tariffs():
    # Создаем подключение к базе данных
    engine = create_engine('postgresql://postgres:postgres@db:5432/tarot_bot')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Создаем тарифы
    tariffs = [
        Tariff(
            name="Базовый",
            description="Доступ к базовым раскладам",
            price=299.0,
            duration_days=30,
            readings_count=5
        ),
        Tariff(
            name="Стандарт",
            description="Доступ ко всем раскладам",
            price=599.0,
            duration_days=30,
            readings_count=15
        ),
        Tariff(
            name="Премиум",
            description="Неограниченный доступ ко всем раскладам",
            price=999.0,
            duration_days=30,
            readings_count=999
        )
    ]

    # Добавляем тарифы в базу данных
    for tariff in tariffs:
        session.add(tariff)

    # Сохраняем изменения
    session.commit()
    session.close()

if __name__ == "__main__":
    init_tariffs() 