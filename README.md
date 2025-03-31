# URL Shortening Service

## Описание

Сервис для сокращения ссылок, разработанный с использованием FastAPI и SQLAlchemy. Этот сервис позволяет пользователям сокращать длинные URL и перенаправлять на оригинальные URL по коротким ссылкам.

## Технологии

- **FastAPI** — для создания REST API.
- **SQLAlchemy** — для работы с базой данных.
- **PostgreSQL** — база данных для хранения сокращённых URL.
- **asyncpg** — асинхронный драйвер для PostgreSQL.
- **Pydantic** — для валидации данных.
- **Uvicorn** — ASGI сервер для запуска FastAPI-приложения.

## Структура проекта

project/

├── main.py # Основной файл приложения 
FastAPI 

├── models.py # Модели SQLAlchemy для базы данных 

├── schemas.py # Pydantic-схемы для входных и выходных данных

├── crud.py # CRUD-операции для работы с базой данных

├── database.py # Подключение к базе данных и настройки сессий 

├── .env # Переменные окружения (строка подключения к базе данных)

├── requirements.txt #Зависимости проекта


## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com//url-shortening-service.git
cd url-shortening-service
```

### 2. Установить зависимости
Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate  # для Windows
```

```bash
pip install -r requirements.txt
```

4. Запуск приложения
Вы можете запустить приложение с помощью Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```
После этого приложение будет доступно по адресу: http://127.0.0.1:8080

## API

1. ### POST/

Сокращает URL и возвращает короткую ссылку.

Запрос:
{
  "original_url": "https://www.example.com"
}

Ответ:
{
  "short_url": "http://127.0.0.1:8080/kDBNzK",
  "original_url": "https://www.example.com"
}

2. ### GET /{short_id}
Перенаправляет на оригинальный URL по короткому идентификатору.

Пример:

Запрос по адресу http://127.0.0.1:8080/kDBNzK перенаправит на оригинальный URL.

3. ### GET /urls/
Получить все сокращённые URL из базы данных.