# Microshop

Backend API для интернет-магазина с авторизацией, ролями, правами доступа, корзиной и заказами.

Проект реализован на **FastAPI** с асинхронной работой с БД, системой ролей и прав (RBAC)  
и покрыт асинхронными тестами с использованием **PostgreSQL**.

---

## Возможности

- Регистрация и авторизация пользователей
- JWT access / refresh токены
- Хранение refresh токена в cookies
- Роли и права доступа (RBAC)
- Управление продуктами (admin / manager)
- Корзина пользователя
- Создание и управление заказами
- Админские эндпоинты
- Асинхронные тесты с отдельной test-базой данных

---

## Технологии

- Python 3.12+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Pydantic v2
- JWT (python-jose)
- Poetry
- pytest / pytest-asyncio
- httpx

---

## Архитектура

Проект построен с чётким разделением ответственности:

- `views` — HTTP слой (эндпоинты)
- `crud` — работа с базой данных
- `schemas` — Pydantic модели
- `core` — конфигурация, безопасность, зависимости
- `tests` — асинхронные тесты с отдельной БД

Права доступа реализованы через **RBAC**:
- роли
- permissions
- ассоциативные таблицы
- dependency factory в FastAPI

---

## Установка и запуск

### 1. Клонировать проект
```bash
git clone https://github.com/your-username/microshop.git
cd microshop
```

### 2. Установить Poetry (если не установлен)
```bash
pip install poetry
```
Проверить:
```bash
poetry --version
```


### 3. Установить зависимости
```bash
poetry install
```
Активировать виртуальное окружение:
```bash
poetry shell
```

### 4. Создать .env файл
```env
DB_URL=postgresql+asyncpg://user:password@localhost:5432/microshop
JWT_SECRET_KEY=super_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```


### 5. Применить миграции
```bash
alembic upgrade head
```

### 6. Запустить приложение
```bash
uvicorn microshop.main:app --reload
```
Swagger будет доступен по адресу:
http://127.0.0.1:8000/docs


## Тесты

Для тестов используется отдельная PostgreSQL база данных
и отдельный `.env.test` файл.

Запуск всех тестов:
```bash
pytest
```

### Тестами покрыты:
- авторизация
- refresh токены
- корзина
- заказы
- права доступа (401 / 403 / 200)
- админские эндпоинты

### Безопасность
- Access токен передаётся через Authorization: Bearer
- Refresh токен хранится в HttpOnly cookies
- Проверка прав доступа через dependency factory
- Чёткое разделение ролей и permissions

## Возможные улучшения

- CI/CD (GitHub Actions)
- Кеширование (Redis)
- Rate limiting
- Версионирование API

⸻

### Статус проекта

Проект завершён и может использоваться как:
	•	учебный backend-проект
	•	основа для реального сервиса
	- пример архитектуры FastAPI + RBAC + tests