import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from celery_app.celery import app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailings_project.settings.prod')
django.setup()

def check_database():
    """Проверка подключения к PostgreSQL через Django ORM"""
    db_conn = connections['default']
    try:
        db_conn.cursor()
        print("✅ PostgreSQL connection: OK")
        return True
    except OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


def check_celery():
    """Проверка, что Celery воркеры доступны"""
    try:
        result = app.control.ping(timeout=5)
        if result:
            print("✅ Celery worker(s) online:", result)
            return True
        print("❌ No Celery workers responded.")
        return False
    except Exception as e:
        print(f"❌ Celery healthcheck failed: {e}")
        return False


if __name__ == "__main__":
    db_ok = check_database()
    celery_ok = check_celery()

    if db_ok and celery_ok:
        print("🟢 All systems operational.")
        exit(0)
    else:
        print("🔴 Health check failed.")
        exit(1)
