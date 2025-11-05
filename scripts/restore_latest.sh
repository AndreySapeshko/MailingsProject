#!/bin/bash
set -e

LATEST_FILE=$(ls -t /backups | head -n 1)
if [ -z "$LATEST_FILE" ]; then
    echo "❌ Нет доступных бэкапов."
    exit 1
fi

echo "🛟 Создаю страховой бэкап перед восстановлением..."
pg_dump -U "$DATABASE_USER" "$DATABASE_NAME" -f "/backups/pre_restore_$(date +%Y-%m-%d_%H-%M-%S).sql"

echo "⚠️  Пересоздаю базу данных $DATABASE_NAME..."
psql -U "$DATABASE_USER" -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${DATABASE_NAME}';"
psql -U "$DATABASE_USER" -d postgres -c "DROP DATABASE IF EXISTS \"${DATABASE_NAME}\";"
psql -U "$DATABASE_USER" -d postgres -c "CREATE DATABASE \"${DATABASE_NAME}\";"

echo "♻️  Восстанавливаю базу данных из $LATEST_FILE..."
psql -U "$DATABASE_USER" "$DATABASE_NAME" < "/backups/$LATEST_FILE"

echo "✅ Восстановление из $LATEST_FILE завершено успешно!"
