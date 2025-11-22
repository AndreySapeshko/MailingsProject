import redis
from django.db import connection
from django.http import JsonResponse
from celery_app.celery import app as celery_app


def health_live(request):
    """Проверка что Django жив."""
    return JsonResponse({"status": "live"}, status=200)


def health_ready(request):
    """Проверка зависимостей: DB, Redis, Celery."""
    checks = {
        "database": False,
        "redis": False,
        "celery": False,
    }

    # Проверяем PostgreSQL
    try:
        connection.cursor()
        checks["database"] = True
    except Exception:
        pass

    # Проверяем Redis
    try:
        r = redis.Redis(
            host="redis",  # либо settings.REDIS_HOST
            port=6379,
            db=0,
            socket_connect_timeout=1,
            socket_timeout=1
        )
        r.ping()
        checks["redis"] = True
    except Exception:
        pass

    # Проверяем Celery
    try:
        result = celery_app.control.ping(timeout=1.0)
        checks["celery"] = bool(result)
    except Exception:
        pass

    overall = all(checks.values())
    status = 200 if overall else 503

    return JsonResponse(
        {
            "status": "ready" if overall else "degraded",
            "checks": checks
        },
        status=status
    )

