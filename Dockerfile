# Используем официальный Python-образ
FROM python:3.12-slim

# Устанавливаем зависимости системы (для psycopg2, Pillow и т.д.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Настройки окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем директорию приложения
WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Команда по умолчанию
CMD ["gunicorn", "mailings_project.wsgi:application", "--bind", "0.0.0.0:8000"]
