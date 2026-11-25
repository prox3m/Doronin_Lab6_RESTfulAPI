# Credit Bank API

RESTful API для управления кредитами и вкладами. Реализовано на Django + Django REST Framework с JWT-аутентификацией и Swagger-документацией.

## Стек

- Django 6.1.3
- Django REST Framework 3.18.0
- djangorestframework-simplejwt (JWT)
- drf-spectacular (Swagger)
- django-cors-headers (CORS)
- PostgreSQL 16
- Gunicorn
- Docker / Docker Compose

## Модели

| Модель | Поля | Связи |
|---|---|---|
| `Credit` | amount, interest_rate, term_months, issued_at, is_active | FK → User |
| `Deposit` | amount, interest_rate, term_months, opened_at, is_active | FK → User |
| `Transaction` | type, amount, created_at | FK → Credit (nullable), FK → Deposit (nullable) |

**Ограничение БД:** `CheckConstraint` на `Transaction` — ровно один из `credit`/`deposit` должен быть заполнен (XOR).

## Быстрый старт

1. Клонировать репозиторий:
   ```bash
   git clone <ссылка>
   cd Lab6_RestAPI
   ```

2. Создать `.env` на основе шаблона:
   ```bash
   cp .env.example .env
   ```
   Заполнить `SECRET_KEY`, `POSTGRES_PASSWORD`.

3. Запустить:
   ```bash
   docker-compose up --build
   ```

4. Создать суперпользователя:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. Открыть Swagger: http://localhost:8000/api/docs/

## Аутентификация (JWT)

### Получить токен

```
POST /api/token/
Body: {"username": "...", "password": "..."}
Response: {"access": "...", "refresh": "..."}
```

### Обновить токен

```
POST /api/token/refresh/
Body: {"refresh": "..."}
```

### Использовать токен

В заголовке каждого запроса:
```
Authorization: Bearer <access_token>
```

## Эндпоинты

| Метод | URL | Действие |
|---|---|---|
| POST | `/api/token/` | Получить JWT |
| POST | `/api/token/refresh/` | Обновить JWT |
| GET/POST | `/api/credits/` | Список / создать кредит |
| GET/PUT/PATCH/DELETE | `/api/credits/{id}/` | CRUD кредита |
| GET/POST | `/api/deposits/` | Список / создать вклад |
| GET/PUT/PATCH/DELETE | `/api/deposits/{id}/` | CRUD вклада |
| GET/POST | `/api/transactions/` | Список / создать транзакцию |
| GET/PUT/PATCH/DELETE | `/api/transactions/{id}/` | CRUD транзакции |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/schema/` | OpenAPI-схема |

## Пагинация

Все list-эндпоинты возвращают по 10 записей:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/credits/?page=2",
  "previous": null,
  "results": [...]
}
```
Параметр: `?page=N`.

## Swagger + Authorize

1. Открыть `http://localhost:8000/api/docs/`
2. Получить токен через `POST /api/token/`
3. Нажать **Authorize** → ввести `Bearer <access_token>` → **Authorize**
4. Выполнять запросы прямо из браузера

## Безопасность

- **JWT-аутентификация** — все эндпоинты (кроме `/api/token/`) требуют токен.
- **Фильтрация по пользователю** — `get_queryset()` возвращает только объекты `request.user`.
- **`perform_create`** — `user` берётся из токена, а не из тела запроса.
- **Валидация транзакций** — сериализатор проверяет XOR и владельца `credit`/`deposit`.
- **`CheckConstraint` в БД** — «последний рубеж», даже через `psql` нельзя создать некорректную транзакцию.
- **Секреты в `.env`** — `.env` в `.gitignore`, в репозитории только `.env.example`.

## Переменные окружения

| Переменная | Назначение |
|---|---|
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Список хостов через запятую |
| `POSTGRES_DB` | Имя базы |
| `POSTGRES_USER` | Пользователь БД |
| `POSTGRES_PASSWORD` | Пароль БД |
| `POSTGRES_HOST` | Хост (`db` внутри Docker) |
| `POSTGRES_PORT` | Порт (`5432`) |
| `CORS_ALLOWED_ORIGINS` | Разрешённые origin'ы (React) |

## Структура проекта

```
credit_bank/
├── credit_bank/          # настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── banking/              # приложение API
│   ├── models.py         # Credit, Deposit, Transaction
│   ├── serializers.py    # сериализаторы с валидацией
│   ├── views.py          # ViewSets
│   └── urls.py           # роутер
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```