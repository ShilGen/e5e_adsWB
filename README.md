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

