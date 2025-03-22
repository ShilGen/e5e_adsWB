import os
import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic.config import Config
from alembic import command
from typing import List, Dict

# Загружаем переменные окружения из файла .env
load_dotenv()

# Настройка SQLAlchemy
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///adverts.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Advert(Base):
    """
    Модель для хранения данных о рекламных кампаниях.
    """
    __tablename__ = 'adverts'

    advertId = Column(Integer, primary_key=True)
    type = Column(Integer)
    status = Column(Integer)
    changeTime = Column(String)

def get_api_token() -> str:
    """
    Получает токен из переменных окружения.
    
    Returns:
        str: Токен для авторизации в API.
    """
    return os.getenv('TOKEN', '')

def fetch_advert_data(token: str) -> Dict:
    """
    Выполняет GET-запрос к API для получения данных о рекламных кампаниях.
    
    Args:
        token (str): Токен для авторизации в API.
    
    Returns:
        Dict: JSON-ответ от API.
    """
    url = "https://advert-api.wildberries.ru/adv/v1/promotion/count"
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверяем успешность запроса
    return response.json()

def create_tables() -> None:
    """
    Создает таблицы в базе данных.
    """
    Base.metadata.create_all(bind=engine)

def insert_advert_data(advert_data: List[Dict]) -> None:
    """
    Вставляет данные о рекламных кампаниях в таблицу.
    
    Args:
        advert_data (List[Dict]): Список словарей с данными о рекламных кампаниях.
    """
    session = SessionLocal()
    try:
        for advert in advert_data:
            db_advert = Advert(
                advertId=advert['advertId'],
                type=advert['type'],
                status=advert['status'],
                changeTime=advert['changeTime']
            )
            session.add(db_advert)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при вставке данных: {e}")
    finally:
        session.close()

def main():
    """
    Основная функция программы.
    """
    token = get_api_token()
    if not token:
        print("Токен не найден в переменных окружения.")
        return
    
    try:
        data = fetch_advert_data(token)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return
    
    advert_list = []
    for advert_group in data.get('adverts', []):
        for advert in advert_group.get('advert_list', []):
            advert_list.append({
                'advertId': advert['advertId'],
                'type': advert_group['type'],
                'status': advert_group['status'],
                'changeTime': advert['changeTime']
            })
    
    #create_tables()
    insert_advert_data(advert_list)
    print("Данные успешно сохранены в базу данных.")

if __name__ == "__main__":
    main()
