# MailingsProject

Сервис для управления e-mail рассылками с веб-интерфейсом и REST API.

## 🚀 Возможности

- Регистрация и авторизация пользователей
- Роли:
  - **Пользователь** – создаёт свои сообщения, получателей и рассылки, видит *только свои* данные
  - **Менеджер** – просмотр объектов всех пользователей и логов, без права изменения
  - **Администратор** – полный доступ
- Управление объектами:
  - **Получатели** (Recipients)
  - **Сообщения** (Messages)
  - **Рассылки** (Mailings)
- Отправка писем:
  - Ручной запуск рассылки `send_now()`
  - Автоматический запуск по расписанию через Celery + Redis + APScheduler
  - Логирование каждой отправки в `MailingLog`
- API:
  - CRUD для сообщений, получателей и рассылок
  - RBAC на уровне API (доступ по ролям)
  - Автогенерация OpenAPI-схемы и документации (Swagger UI, ReDoc)
- Инфраструктура:
  - Docker + docker-compose (web + db + redis + celery + celery-beat)
  - Healthcheck для Django, PostgreSQL и Celery
  - Логирование в файлы (`logs/django.log`, `logs/celery.log` и т.д.)
  - Набор тестов (pytest + pytest-django + factory_boy)

---

## 🧱 Стек

- Python 3.12 / 3.13
- Django
- Django REST Framework
- Celery + Redis
- PostgreSQL
- APScheduler / django-apscheduler
- drf-spectacular (OpenAPI)
- Docker, docker-compose
- pytest, factory_boy

---

## 📦 Структура проекта (основные приложения)

- `mailings` – модели и логика рассылок
  - `Mailing`, `Message`, `MailingLog`
  - `send_now()`, Celery-задачи `process_mailings`
- `recipients` – получатели рассылок
- `users` / `accounts` – кастомный пользователь и работа с профилем
- `api` – REST API (ViewSet’ы, сериализаторы, permissions)
- `scheduler` – планировщик на базе APScheduler
- `celery_app` – конфигурация Celery
- `core` – общие миксины, кеш, сигналы
- `mailings_project` – Django-конфигурация, healthcheck

---

## ⚙️ Запуск в Docker (dev/prod)

### Quick Start

### Clone the repository
```bash
git clone <https://github.com/AndreySapeshko/MailingsProject>
cd MailingsProject
```

### 1. Подготовка `.env`

Создай файл `.env` в корне проекта, например:


DJANGO_ENV=prod 

SECRET_KEY=your-secret-key
DATABASE_NAME=mailings_project
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

ALLOWED_HOSTS=127.0.0.1,localhost

для healthcheck’ов и логики ролей/пермишенов свои переменные, если есть
### 2. Сборка и запуск
bash
Копировать код
docker compose up -d --build
Поднимутся сервисы:

web – Django + Gunicorn

db – PostgreSQL

redis – Redis

celery – Celery worker

celery-beat – Celery beat / планировщик

(при наличии) nginx / обратный прокси

### 3. Миграции и суперпользователь
Если в command контейнера web миграции не запускаются автоматически:

bash
Копировать код
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
### 🌐 Веб-интерфейс и API
После запуска по умолчанию:

Веб-интерфейс: http://localhost:8000/

Админка: http://localhost:8000/admin/

Личный кабинет / работа с рассылками – через соответствующие views в mailings, recipients, users

### 📘 OpenAPI / Swagger / ReDoc
OpenAPI-схема: GET /api/schema/

Swagger UI: GET /api/docs/

ReDoc: GET /api/redoc/

(пути зависят от твоего urls.py, при необходимости поправь их здесь)

### 🔐 Роли и права (RBAC)
Роль хранится в кастомной модели пользователя, типовые значения:

user

manager

admin

Права реализованы через RoleBasedAccessPermission (в api.permissions) и AccessByRoleMixin для обычных Django-view.

Общая логика:

user

видит только свои объекты (Mailing, Message, Recipient)

может создавать / редактировать / удалять только свои объекты

manager

может просматривать объекты всех пользователей (read-only)

изменение запрещено (кроме случаев, явно разрешённых)

admin

полный доступ ко всем объектам

### 📬 Логика рассылок
**Модели**

Message(subject, body, user)

Recipient(email, name, is_active, user)

Mailing:

name

date_first_dispatch

dispatch_end_date

periodicity (once, daily, weekly)

status (created, launched, completed, stopped)

recipients (ManyToMany с Recipient)

message (ForeignKey на Message)

user (владелец рассылки)

MailingLog – запись о попытке отправки:

mailing, recipient, timestamp, status (success / failed), server_response, user

**Отправка**

Метод модели:

mailing.send_now()

Celery-задача:

process_mailings.delay() 
 process_mailings:

выбирает активные рассылки по времени и статусу

вызывает send_now() для каждой

логирует успех/ошибки

**Планировщик**

APScheduler (scheduler/scheduler.py) раз в минуту вызывает:

run_mailing_tasks()  # внутри -> process_mailings.delay()
Планировщик стартует при запуске Django (учитывается RUN_MAIN, чтобы не запускать его дважды).

**❤️ Healthcheck**

Скрипт mailings_project/healthcheck.py
Проверяет:

подключение к базе (check_database())

доступность Celery-воркеров (check_celery() с app.control.ping())

Коды возврата:

0 – всё OK

1 – что-то не работает

URL-проверка
В проекте есть API-точка здоровья (например, /health/), которая:

проверяет БД и Redis

может дополнительно пинговать Celery

возвращает JSON:

`{
  "status": "ok",
  "database": true,
  "redis": true,
  "celery": true
}`

### 🧪 Тестирование
Используется pytest + pytest-django + factory_boy.

Запуск тестов:

`docker compose exec web pytest -v`

**Основные группы тестов:**

mailings/tests/

test_send_now.py – логика send_now

test_recipient_selection.py – выбор активных получателей

test_tasks.py – Celery-задачи ping_celery, process_mailings

test_views.py – веб-представления рассылок

recipients/tests/ – фабрики и тесты получателей

scheduler/tests/test_scheduler.py – планировщик run_mailing_tasks

api/tests/

test_recipients_api.py, test_messages_api.py, test_mailings_api.py

rbac/ – тесты прав доступа для разных ролей

### 🧰 Полезные команды (Makefile)
В проекте есть Makefile (при необходимости дополни):

`run`:
\tdocker compose up -d --build

`down`:
\tdocker compose down

`logs`:
\tdocker compose logs -f

`test`:
\tdocker compose exec web pytest -v

`migrate`:
\tdocker compose exec web python manage.py migrate

`superuser`:
\tdocker compose exec web python manage.py createsuperuser

`health`:
\tdocker compose exec web python mailings_project/healthcheck.py


---

# 🚀 Деплой (Production Deployment)

Проект поддерживает полноценный production-деплой с использованием:

* **Docker + Docker Compose**
* **Gunicorn**
* **Nginx**
* **PostgreSQL**
* **Redis**
* **Celery + Celery Beat**
* **Статических файлов на volume**

Ниже — пошаговая инструкция.

---

## 1. 📁 Структура папок

Проект ожидает следующую структуру:

```
MailingsProject/
│
├── deploy/
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   ├── entrypoint.sh
│   └── .env
│
├── Dockerfile.prod
├── requirements.txt
└── ...
```

⚠️ **Важно:** переменные окружения должны быть в `deploy/.env`.

---

## 2. ⚙️ Файл окружения `.env`

Пример содержимого:

```
DJANGO_ENV=prod
DEBUG=False
SECRET_KEY=your-production-secret-key

DATABASE_NAME=mailings_project
DATABASE_USER=postgres_user
DATABASE_PASSWORD=postgres_pass
DATABASE_HOST=db
DATABASE_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
```

---

## 3. 🧱 Сборка Production-образа

Перейдите в директорию `deploy/`:

```bash
cd deploy
```

Чтобы собрать образы:

```bash
docker compose --env-file .env -f docker-compose.prod.yml build
```

(или **с чистого листа**)

```bash
docker compose --env-file .env -f docker-compose.prod.yml build --no-cache
```

---

## 4. 🚀 Запуск проекта

```bash
docker compose --env-file .env -f docker-compose.prod.yml up -d
```

Проверить статус:

```bash
docker compose -f docker-compose.prod.yml ps
```

При успешном запуске должны работать контейнеры:

* `web` — Gunicorn + Django
* `nginx`
* `db` — PostgreSQL
* `redis`
* `celery`
* `beat`
* `worker` (опционально)
* `static_volume`, `media_volume`, `postgres_data`

---

## 5. 🗄️ Миграции + сбор статических файлов

После первого деплоя:

```bash
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

---

## 6. 🧪 Проверка Healthcheck API

Открыть в браузере:

```
http://localhost/api/health/
```

Или через curl:

```bash
curl http://localhost/api/health/
```

---

## 7. 📡 Production-URL

Если деплой локально:

```
http://localhost
```

Если на сервере:

```
http://<SERVER_IP>
```

---

## 8. 🔄 Перезапуск и остановка

Перезапуск:

```bash
docker compose -f docker-compose.prod.yml restart
```

Остановка:

```bash
docker compose -f docker-compose.prod.yml down
```

Полная остановка + очистка volume:

```bash
docker compose -f docker-compose.prod.yml down -v
```

---

## 9. 🛡️ Защита: как подготовиться

После деплоя стоит проверить:

* доступность API `/api/health/`
* работу Celery и Celery beat
* правильность статики `/static/`
* корректность пересоздания контейнеров
* отсутствующие ошибки в логах:

```bash
docker compose -f docker-compose.prod.yml logs -f web
```

---

