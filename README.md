# Task Manager

<div align="center">

**Полнофункциональный менеджер задач с REST API, CLI и современным SPA-фронтендом**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-база_данных-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00.svg?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Лицензия](https://img.shields.io/badge/лицензия-MIT-green.svg)](LICENSE)

</div>

---

## О проекте

Task Manager — production-grade приложение для организации задач и групп. Объединяет **RESTful API** на FastAPI, интерактивный **CLI-инструмент** и адаптивный **React SPA** фронтенд. Всё это работает поверх PostgreSQL с чистой доменно-ориентированной архитектурой.

### Почему этот проект примечателен

- **Три интерфейса — одно ядро** — один и тот же сервисный слой обслуживает CLI, REST API и веб-интерфейс
- **Доменно-ориентированный дизайн** — бизнес-логика живёт в чистых Python-объектах предметной области, полностью отделённых от инфраструктуры
- **Надёжная обработка ошибок** — собственная иерархия исключений со структурированными ответами API и детальным логированием
- **Полный CRUD с фильтрацией и сортировкой** — получение задач/групп по любому полю, фильтрация по статусу и группе
- **Inline-редактирование** — редактирование записей прямо в строках таблицы без выхода из контекста
- **Модальные окна подтверждения** — операции удаления защищены диалогами подтверждения
- **Авто-миграция при запуске** — SQLAlchemy создаёт таблицы автоматически, также автоматически создаётся группа по умолчанию

---

## Архитектура

```
┌─────────────────────────────────────────────────────┐
│                   CLI / REST / SPA                   │  ← Представление
├─────────────────────────────────────────────────────┤
│                 Сервисный слой                        │  ← Бизнес-логика
│                (TaskManager)                         │
├─────────────────────────────────────────────────────┤
│                 Доменная модель                       │  ← Чистый Python
│                (Task, Group)                         │
├─────────────────────────────────────────────────────┤
│                 Репозиторий                           │  ← Доступ к данным
│                (ORMManager)                          │
├─────────────────────────────────────────────────────┤
│                 PostgreSQL                           │  ← Хранение
│                (SQLAlchemy ORM)                      │
└─────────────────────────────────────────────────────┘
```

### Структура проекта

```
task-manager/
├── api/                    # Слой FastAPI REST
│   ├── routes/             #   Эндпоинты: tasks, groups, pages
│   ├── schemas/            #   Pydantic-модели запросов/ответов
│   ├── handlers/           #   Пользовательские обработчики исключений
│   └── dependencies.py     #   Внедрение сервиса
├── cli/                    # Консольный интерфейс
│   ├── app.py              #   Интерактивное CLI-приложение
│   ├── cli_argparser.py    #   Парсинг аргументов
│   └── cli_output.py       #   Форматированный вывод
├── config/                 # Конфигурация и логирование
├── domain/                 # Чистые сущности предметной области (Task, Group)
├── exceptions/             # Пользовательская иерархия исключений
├── repository/             # Слой доступа к данным
│   ├── models/             #   Модели SQLAlchemy ORM
│   ├── orm_manager.py      #   Реализация репозитория
│   └── session_context_manager.py  # Контекст транзакций
├── services/               # Бизнес-логика (TaskManager)
├── frontend/               # React SPA (Vite)
│   └── src/
│       ├── components/     #   TaskList, GroupList, формы, ConfirmModal
│       ├── services/       #   Axios-клиент для API
│       └── App.jsx         #   Главный компонент приложения
├── templates/              # Jinja2-шаблоны для серверного рендеринга
├── main_web.py             # Точка входа FastAPI
├── main_cli.py             # Точка входа CLI
└── requirements.txt
```

---

## Возможности

### Задачи
| Операция | CLI | API | Веб-интерфейс |
|-----------|:---:|:---:|:------:|
| Создание | ✓ | ✓ | ✓ |
| Просмотр (сортировка по ID, названию, статусу, группе) | ✓ | ✓ | ✓ |
| Фильтрация по статусу и группе | — | ✓ | ✓ |
| Обновление (PATCH) | ✓ | ✓ | ✓ (inline) |
| Удаление | ✓ | ✓ | ✓ (с подтверждением) |

### Группы
| Операция | CLI | API | Веб-интерфейс |
|-----------|:---:|:---:|:------:|
| Создание | ✓ | ✓ | ✓ |
| Просмотр (сортировка по ID, названию) | ✓ | ✓ | ✓ |
| Отображение связанных задач | — | ✓ | ✓ (в таблице) |
| Обновление (PATCH) | ✓ | ✓ | ✓ (inline) |
| Удаление (задачи переносятся в default group) | ✓ | ✓ | ✓ (с подтверждением) |

### Технические особенности

- **Статусы**: `active`, `frozen`, `finished` — с цветовой кодировкой в UI (красный/синий/зелёный)
- **Валидация**: ограничения длины названий (50 символов для задач, 25 для групп), допустимые статусы, проверка существования группы
- **Каскад при удалении группы**: задачи переназначаются в `default group` вместо того, чтобы остаться без группы
- **Защита от дублирования**: названия групп должны быть уникальными (с учётом регистра)
- **Логирование**: настраивается через `.env` (от `DEBUG` до `CRITICAL`)
- **CORS**: настроен для Vite dev-сервера

---

## Быстрый старт

### Требования

- **Python** 3.10+
- **PostgreSQL** 14+
- **Node.js** 18+ (для фронтенда)
- **pip** и **npm**

### 1. Клонирование и настройка окружения

```bash
git clone https://github.com/delagranger/task-manager.git
cd task-manager

# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate
# Активация (Linux / macOS)
source venv/bin/activate

# Установка Python-зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта (см. `.env.example`):

```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=task_manager
LOG_LEVEL=INFO
```

### 3. Запуск бэкенда

```bash
# Запуск FastAPI-сервера с авто-перезагрузкой
python -m uvicorn main_web:app --host 0.0.0.0 --port 8000 --reload
```

API доступно по адресу `http://localhost:8000`.

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 4. Запуск фронтенда

```bash
cd frontend
npm install
npm run dev
```

Откройте `http://localhost:5173` (или `:5174`) в браузере.

### 5. Использование CLI

```bash
python main_cli.py --help
python main_cli.py add-task -t "Купить продукты" -s active -g "личное"
python main_cli.py add-group -t "работа"
python main_cli.py list-tasks -s status
```

---

## Обзор API

| Метод | Эндпоинт | Описание |
|--------|----------|-------------|
| `GET` | `/api/v1/tasks/` | Список задач (параметры: `sort_type`, `filtered`, `status`, `group`) |
| `POST` | `/api/v1/tasks/` | Создать задачу |
| `PATCH` | `/api/v1/tasks/{id}/` | Обновить задачу |
| `DELETE` | `/api/v1/tasks/{id}/` | Удалить задачу |
| `GET` | `/api/v1/groups/` | Список групп (параметр: `sort_type`) |
| `POST` | `/api/v1/groups/` | Создать группу |
| `PATCH` | `/api/v1/groups/{id}/` | Переименовать группу |
| `DELETE` | `/api/v1/groups/{id}/` | Удалить группу (задачи → default group) |
| `GET` | `/` | Серверный рендеринг страницы задач (Jinja2) |
| `GET` | `/groups` | Серверный рендеринг страницы групп (Jinja2) |

Все ответы — в формате JSON. Ошибки следуют единому формату `{ "detail": "..." }`.

---

## Технологический стек

| Слой | Технология |
|-------|-----------|
| **Бэкенд-фреймворк** | FastAPI (Starlette + Pydantic v2) |
| **ORM** | SQLAlchemy 2.0 с `joinedload` для жадной загрузки |
| **База данных** | PostgreSQL (через `psycopg2-binary`) |
| **Фронтенд** | React 19 + Vite 8 |
| **HTTP-клиент** | Axios |
| **Серверный рендеринг** | Jinja2-шаблоны |
| **CLI** | Click + argparse |
| **Конфигурация** | python-dotenv |
| **Логирование** | Стандартный модуль `logging` с настраиваемыми уровнями |

---

## Архитектурные решения

- **Паттерн Repository** — `ORMManager` абстрагирует все операции с базой данных за чистым интерфейсом, что позволяет легко заменить PostgreSQL на другое хранилище
- **Контекстный менеджер сессий** — `session_scope` гарантирует корректный жизненный цикл commit/rollback, предотвращая утечки соединений
- **Пользовательские исключения** — `TIDNotFound`, `GIDNotFound`, `GroupAlreadyExists`, `StatusNotFound`, `SortTypeNotFound`, `FilterNotExists`, `IncorrectLength` — каждое сопоставлено с соответствующим HTTP-кодом
- **Группа по умолчанию** — всегда присутствует, служит резервной группой для неназначенных и осиротевших задач
- **Семантика PATCH** — только частичные обновления; отсутствующие поля остаются без изменений
- **Жадная загрузка** — `joinedload` устраняет проблему N+1 запросов при получении задач с их группами и групп с их задачами

---

## Лицензия

MIT