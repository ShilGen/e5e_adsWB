#Репозиторий для сбора данных о рекламных кампаниях Wildberries

Этот репозиторий содержит скрипт для сбора данных о рекламных кампаниях с API Wildberries и сохранения их в базу данных SQLite с использованием SQLAlchemy и Alembic для управления миграциями.

Реализовано: Получение списка рекламных кампаний WB API

Требования 

- Python 3.8+
- Установленные зависимости из requirements.txt
     
Создайте файл .env в корневой директории проекта и добавьте токен и URL базы данных:
```
TOKEN=your_token_here
DATABASE_URL=sqlite:///adverts.db
```

Activate a virtual environment
```bash
source .venv/bin/activate
```
Deactivate a virtual environment
```bash
deactivate
```
Install packages using pip and requirements file
```bash
python3 -m pip install -r requirements.txt
```
##Дополнительные шаги 

Инициализация Alembic  
```bash 
alembic init alembic
```

Создание первой миграции  

```bash
alembic revision --autogenerate -m "create initial tables"
```
Применение миграций  
```bash
alembic upgrade head
``` 
Запуск скрипта
```bash
python main.py
```     
     
### Структура проекта 
 
```
.
├── alembic/
│   ├── versions/
│   │   └── ... (файлы миграций)
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── main.py
├── requirements.txt
└── .env
```

Автор: ShilGen
