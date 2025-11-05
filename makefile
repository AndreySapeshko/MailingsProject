include .env
.PHONY: backup backups restore restore-latest clean-backups
# export $(shell sed 's/=.*//' .env)

# Makefile для проекта Mailings Project

PROJECT_NAME=mailingsproject
BACKUP_DIR=backups
DATE=$(shell date +"%Y-%m-%d_%H-%M-%S")

# 🧱 Построить контейнеры
build:
	docker compose build

# 🚀 Запустить проект в фоне
up:
	docker compose up -d

# 🛑 Остановить и удалить контейнеры
down:
	docker compose down

# 🔁 Перезапустить проект
restart:
	docker compose down
	docker compose up -d

# 📜 Логи
logs:
	docker compose logs -f

# 🐚 Войти внутрь web-контейнера
shell:
	docker compose exec web bash

# 🎨 Собрать статику
collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

# ⚙️ Применить миграции
migrate:
	docker compose exec web python manage.py migrate

# 📦 Создать миграции
makemigrations:
	docker compose exec web python manage.py makemigrations

# 👑 Создать суперпользователя
createsuperuser:
	docker compose exec web python manage.py createsuperuser

# 🧹 Полная очистка (контейнеры + volume’ы)
clean:
	docker compose down -v

# 🔍 Проверить статус контейнеров
ps:
	docker compose ps

# 🧠 Проверить настройки Django
check:
	docker compose exec web python manage.py check


# === Управление резервными копиями базы данных ======================
#  make backup                — создать новый бэкап (с автоочисткой старых)
#  make backups               — показать список бэкапов
#  make restore FILE=name.sql — восстановить базу из выбранного бэкапа (со страховкой)
#  make restore-latest        — восстановить из самого свежего бэкапа (со страховкой)
#  make clean-backups         — удалить бэкапы старше 7 дней
# ====================================================================


# 💾 Сделать резервную копию базы данных
backup:
	@echo Backing up database...
	@docker compose exec -T db sh -c 'pg_dump -U "$$DATABASE_USER" "$$DATABASE_NAME" -f /backups/backup_$$(date +%Y-%m-%d_%H-%M-%S).sql'
	@echo Backup saved into /backups inside the container (volume "backups")

# 📜 Показать список доступных бэкапов
backups:
	@echo "📜 Доступные бэкапы:"
	@docker compose exec db bash -c "ls -lh /backups || echo '❌ Папка /backups пуста или недоступна'"

# ♻️ Восстановить базу из указанного файла (со страховкой)
restore:
	@echo "🛟 Создаю страховой бэкап перед восстановлением..."
	docker compose exec -T db bash -c "pg_dump -U $$DATABASE_USER $$DATABASE_NAME -f /backups/pre_restore_$$(date +%Y-%m-%d_%H-%M-%S).sql"
	@echo "⚠️  Пересоздаю базу данных $$DATABASE_NAME..."
	docker compose exec -T db bash -c "psql -U $$DATABASE_USER -d postgres -c 'DROP DATABASE IF EXISTS \"'$$DATABASE_NAME'\";' && psql -U $$DATABASE_USER -d postgres -c 'CREATE DATABASE \"'$$DATABASE_NAME'\";'"
	@echo "♻️  Восстанавливаю базу данных из $(FILE)..."
	docker compose exec -T db bash -c "psql -U $$DATABASE_USER $$DATABASE_NAME < /backups/$(FILE)"
	@echo "✅ Восстановление завершено успешно!"


# 🕓 Восстановить из самого нового бэкапа (со страховкой)
restore-latest:
	@echo "🕓 Ищу последний бэкап и запускаю восстановление..."
	@docker compose exec db bash /app/scripts/restore_latest.sh

# 🧹 Очистка старых бэкапов (по умолчанию старше 7 дней)
clean-backups:
	@echo "🧹 Удаляю старые бэкапы (старше 7 дней)..."
	@docker compose exec db bash -c "find /backups -type f -name '*.sql' -mtime +7 -exec rm -v {} \; || true"
	@echo "✨ Очистка завершена."