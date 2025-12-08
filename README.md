## Установка
Создаём виртуальное окружение:
python -m venv venv

Активируем виртуальное окружение:  
Windows: venv\Scripts\activate  
Linux: source venv/bin/activate

Устанавливаем зависимости:
pip install -r requirements.txt  

## Настройка базы данных
В файле app/db/database.py укажите параметры подключения:
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/inventory_db"

## Запуск сервера
uvicorn app.main:app --reload

## Примеры API
После запуска сервера вы можете открыть документацию в браузере:

http://127.0.0.1:8000/docs/

На этой странице можно:

Просмотреть все доступные API-эндпоинты.

Посмотреть модели запросов и ответов.

Тестировать API-запросы из браузера.
