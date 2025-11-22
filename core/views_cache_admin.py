from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
import redis
from django.conf import settings
from django.http import JsonResponse


# ✅ Проверка: доступ только суперпользователям и администраторам
def admin_check(user):
    return user.is_authenticated and (user.is_superuser or getattr(user, "role", None) == "admin")


@login_required
@user_passes_test(admin_check)
def cache_status_view(request):
    """Простая страница для просмотра ключей кеша и очистки."""
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True)

    message = None

    # Очистка кеша
    if request.method == "POST":
        r.flushdb()
        message = "🧹 Кеш очищен успешно!"

    keys = []
    for key in r.keys("*"):
        ttl = r.ttl(key)
        keys.append({
            "key": key,
            "ttl": ttl if ttl and ttl > 0 else "∞",
        })

    context = {
        "keys": sorted(keys, key=lambda k: k["key"]),
        "count": len(keys),
        "message": message,
        "time": timezone.now(),
    }
    return render(request, "core/cache_status.html", context)


@login_required
@user_passes_test(admin_check)
def cache_status_json(request):
    """Возвращает текущее состояние кеша (для AJAX-обновления)."""
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True)

    keys = []
    for key in r.keys("*"):
        ttl = r.ttl(key)
        keys.append({
            "key": key,
            "ttl": ttl if ttl and ttl > 0 else "∞",
        })

    return JsonResponse({
        "keys": sorted(keys, key=lambda k: k["key"]),
        "count": len(keys),
        "time": timezone.now().strftime("%H:%M:%S"),
    })
