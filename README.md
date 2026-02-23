# Finely — Приложение для управления личными финансами

## Содержание

1. [Описание проекта](#описание-проекта)
2. [Технологический стек](#технологический-стек)
3. [Архитектура](#архитектура)
4. [Установка и запуск](#установка-и-запуск)
5. [Структура проекта](#структура-проекта)
6. [API Endpoints](#api-endpoints)
7. [Модели данных](#модели-данных)
8. [Аутентификация и авторизация](#аутентификация-и-авторизация)
9. [Фронтенд](#фронтенд)
10. [Будущие улучшения](#будущие-улучшения)

---

## Описание проекта

**Finely** — это веб-приложение для учёта личных финансов, разработанное в качестве учебного портфолио-проекта. Приложение позволяет пользователям:

- Регистрироваться и авторизовываться в системе
- Создавать категории доходов и расходов
- Добавлять транзакции с привязкой к категориям
- Просматривать статистику и аналитику
- Получать простые финансовые советы

### Основные функции

| Функция | Описание |
|---------|----------|
| Регистрация/Вход | Создание аккаунта и аутентификация через JWT |
| Категории | Создание, редактирование, удаление и поиск категорий |
| Транзакции | Добавление доходов/расходов с фильтрацией и пагинацией |
| Статистика | Общий баланс, доходы, расходы за период |
| Сравнение | Динамика по сравнению с предыдущим периодом |

---

## Технологический стек

### Backend

| Технология | Назначение |
|------------|------------|
| **FastAPI** | Веб-фреймворк |
| **SQLAlchemy (async)** | ORM для работы с БД |
| **PostgreSQL** | Реляционная база данных |
| **python-jose** | Работа с JWT токенами |
| **passlib** | Хеширование паролей |
| **aiosqlite** | Асинхронный драйвер для SQLite (разработка) |
| **asyncpg** | Асинхронный драйвер для PostgreSQL |

### Frontend

| Технология | Назначение |
|------------|------------|
| **HTML5/CSS3** | Разметка и стилизация |
| **Vanilla JavaScript** | Клиентская логика |
| **Chart.js** | Визуализация данных |
| **Google Fonts** | Шрифты (Syne, DM Sans) |

---

## Архитектура

Проект построен по принципам **Clean Architecture** с чётким разделением слоёв:

```
app/
├── api/              # API endpoints (Router)
│   └── v1/
│       ├── user.py
│       ├── category.py
│       ├── transaction.py
│       └── statistics.py
├── models/           # Модели данных (SQLAlchemy)
│   ├── user.py
│   ├── category.py
│   ├── transaction.py
│   └── token.py
├── schemas/          # Pydantic схемы валидации
├── services/         # Бизнес-логика
├── dependencies/     # Dependency Injection
├── utils/            # Вспомогательные утилиты
├── database/         # Конфигурация БД
├── config.py         # Конфигурация приложения
└── main.py           # Точка входа
```

### Слои приложения

1. **API Layer** — обработка HTTP запросов, валидация через Pydantic
2. **Service Layer** — бизнес-логика
3. **Repository Layer** — работа с БД через SQLAlchemy
4. **Model Layer** — определение таблиц и связей

---

## Установка и запуск

### Требования

- Python 3.10+
- PostgreSQL 15 (или SQLite для разработки)
- Node.js (не требуется, фронтенд статический)

### Быстрый старт

#### 1. Клонирование и настройка

```bash
# Клонирование репозитория
git clone <repo-url>
cd <project-folder>

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
cd app
pip install -r requirements.txt
```

#### 2. Настройка базы данных

**Вариант А: PostgreSQL (рекомендуется для продакшена)**

```bash
# Запуск PostgreSQL через Docker
cd app
docker-compose up -d db
```

Измените `config.py`:
```python
DATABASE_URL = 'postgresql+asyncpg://user:password@localhost:5432/finance_db'
```

**Вариант Б: SQLite (для разработки)**

```python
DATABASE_URL = 'sqlite+aiosqlite:///finance.db'
```

#### 3. Запуск сервера

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. Запуск фронтенда

Просто откройте `frontend/home.html` в браузере или используйте простой сервер:

```bash
# Python
python -m http.server 8080 --directory frontend

# или Node.js
npx serve frontend
```

> **Важно:** При использовании файловой схемы (`file://`) некоторые функции могут работать некорректно. Рекомендуется использовать локальный HTTP-сервер.

---

## Структура проекта

```
project-root/
├── app/                      # Backend (FastAPI)
│   ├── api/
│   │   └── v1/
│   │       ├── user.py       # Эндпоинты пользователей
│   │       ├── category.py   # Эндпоинты категорий
│   │       ├── transaction.py# Эндпоинты транзакций
│   │       └── statistics.py # Эндпоинты статистики
│   ├── models/               # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── token.py
│   ├── schemas/              # Pydantic схемы
│   ├── services/             # Бизнес-логика
│   ├── dependencies/         # Dependency Injection
│   ├── utils/                # Утилиты и исключения
│   ├── database/
│   │   └── db.py             # Конфигурация БД
│   ├── config.py             # Конфигурация
│   ├── main.py               # Точка входа
│   ├── requirements.txt      # Зависимости Python
│   └── docker-compose.yml    # PostgreSQL
├── frontend/                 # Frontend (Static HTML)
│   ├── home.html             # Главная страница
│   ├── auth.html             # Авторизация/Регистрация
│   ├── dashboard.html        # Дашборд
│   ├── transactions.html     # Список транзакций
│   └── categories.html       # Управление категориями
└── docs/                     # Документация
    └── README.md
```

---

## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/api/v1/register` | Регистрация нового пользователя |
| `POST` | `/api/v1/login` | Вход в аккаунт |
| `POST` | `/api/v1/logout` | Выход из аккаунта |
| `POST` | `/api/v1/refresh` | Обновление токенов |
| `GET` | `/api/v1/profile` | Получение профиля пользователя |

### Категории

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/api/v1/category/create` | Создание категории |
| `GET` | `/api/v1/category/` | Список категорий (с фильтрацией) |
| `GET` | `/api/v1/category/{id}` | Категория по ID |
| `PATCH` | `/api/v1/category/{id}` | Обновление категории |
| `DELETE` | `/api/v1/category/{id}` | Удаление категории |

### Транзакции

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/api/v1/transactions/create` | Создание транзакции |
| `GET` | `/api/v1/transactions/` | Список транзакций (с фильтрацией) |
| `GET` | `/api/v1/transactions/{id}` | Транзакция по ID |
| `DELETE` | `/api/v1/transactions/{id}` | Удаление транзакции |

### Статистика

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/statistics/` | Получение статистики за период |

#### Параметры статистики

- `period` — период выборки: `day`, `week`, `month`, `year`

### Системные

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/` | Проверка здоровья API |

---

## Модели данных

### User (Пользователь)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный ID |
| `login` | String | Уникальный логин |
| `hashed_password` | String | Хешированный пароль |
| `created_at` | DateTime | Дата создания |
| `categories` | Relationship | Связь с категориями |
| `transactions` | Relationship | Связь с транзакциями |

### Category (Категория)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный ID |
| `name` | String | Название категории |
| `category_type` | String | Тип: `income` или `expense` |
| `user_id` | Integer | ID владельца (FK) |
| `transactions` | Relationship | Связь с транзакциями |

> Уникальный ключ: `name` + `user_id` (однако, в рамках одного пользователя могут быть категории с одинаковым названием, но разным типом)

### Transaction (Транзакция)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный ID |
| `name` | String | Название транзакции |
| `transaction_type` | String | Тип: `income` или `expense` |
| `amount` | Float | Сумма |
| `created_at` | DateTime | Дата создания |
| `category_id` | Integer | ID категории (FK) |
| `user_id` | Integer | ID владельца (FK) |

### TokenBlacklist (Чёрный список токенов)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | Integer | Уникальный ID |
| `token` | String | Токен в чёрном списке |
| `created_at` | DateTime | Дата добавления |

---

## Аутентификация и авторизация

### JWT Токены

Приложение использует пару токенов:

1. **Access Token** — короткоживущий токен (15 минут) для доступа к защищённым ресурсам
2. **Refresh Token** — долгоживущий токен (7 дней) для обновления пары токенов

### Flow аутентификации

```
1. Регистрация:
   POST /api/v1/register
   → Создание пользователя
   → Генерация пары токенов
   → Возврат токенов клиенту

2. Вход:
   POST /api/v1/login
   → Верификация пароля
   → Генерация пары токенов
   → Возврат токенов клиенту

3. Доступ к защищённым ресурсам:
   GET /api/v1/category/
   → Header: Authorization: Bearer <access_token>
   → Проверка токена
   → Возврат данных

4. Обновление токенов:
   POST /api/v1/refresh
   → Валидация refresh_token
   → Генерация новой пары токенов

5. Выход:
   POST /api/v1/logout
   → Добавление refresh_token в чёрный список
```

### Защита пароля

Пароли хешируются с использованием **bcrypt** через `passlib`:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

---

## Фронтенд

### Страницы

| Файл | Описание |
|------|----------|
| `home.html` | Главная страница с описанием приложения |
| `auth.html` | Формы входа и регистрации |
| `dashboard.html` | Основная страница с статистикой |
| `transactions.html` | Управление транзакциями |
| `categories.html` | Управление категориями |

### Особенности реализации

- **Дизайн:** Тёмная тема с неоновыми акцентами (зелёный, розовый, жёлтый)
- **Анимации:** Aurora background effect на Canvas
- **Шрифты:** Syne (заголовки), DM Sans (текст)
- **Взаимодействие:** AJAX запросы к API без перезагрузки страницы
- **Токены:** Хранятся в `localStorage`
- **Автообновление токенов:** При 401 автоматически обновляет пару токенов

### Пример API запроса с авторизацией

```javascript
const API_BASE = 'http://127.0.0.1:8000';

async function fetchWithAuth(url, options = {}) {
  const token = localStorage.getItem('access_token');
  
  options.headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`
  };
  
  let response = await fetch(API_BASE + url, options);
  
  // Автообновление токена при 401
  if (response.status === 401) {
    const newToken = await refreshTokens();
    if (!newToken) {
      location.href = 'auth.html';
      return;
    }
    options.headers['Authorization'] = `Bearer ${newToken}`;
    response = await fetch(API_BASE + url, options);
  }
  
  return response;
}
```

---

## Будущие улучшения

### Backend

- [ ] Добавить валидацию email при регистрации
- [ ] Реализовать подтверждение email
- [ ] Добавить пагинацию для всех списковых эндпоинтов
- [ ] Реализовать экспорт данных (CSV, PDF)
- [ ] Добавить автоматические бэкапы БД
- [ ] Реализовать rate limiting
- [ ] Добавить логирование (structlog)
- [ ] Написать unit-тесты

### Frontend

- [ ] Переписать на React/Vue
- [ ] Добавить PWA поддержку
- [ ] Мобильная адаптация
- [ ] Тёмная/светлая тема
- [ ] Добавить анимации переходов

### DevOps

- [ ] Docker-compose для полного стека
- [ ] GitHub Actions для CI/CD
- [ ] Настройка HTTPS
- [ ] Мониторинг и алертинг

---

## Лицензия

MIT License

---

## Контакты

Проект разработан в учебных целях для портфолио.

*Backend Developer: [Увиков Дмитрий]*
*Frontend: Сгенерирован с помощью AI*
