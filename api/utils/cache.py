from django.core.cache import cache
from functools import wraps
import hashlib
import json

from rest_framework.response import Response


def make_cache_key(request, prefix="api"):
    """
    Генерирует уникальный ключ для запроса на основе URL, пользователя и параметров.
    """
    base = f"{prefix}:{request.get_full_path()}:{request.user.id}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def cache_response(timeout=60):
    """
    Декоратор для кеширования ответов DRF (Response.data)
    Применяется к методам list() или retrieve() во ViewSet.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if request.method != "GET":
                return func(self, request, *args, **kwargs)

            cache_key = make_cache_key(request)
            cached_data = cache.get(cache_key)
            if cached_data is not None and cached_data != b'':
                print(f"⚡ Кеш API: {cache_key}")
                return Response(cached_data)

            response = func(self, request, *args, **kwargs)
            # Проверяем, что это Response с сериализованными данными
            try:
                cache.set(cache_key, response.data, timeout=timeout)
            except Exception as e:
                print(f"⚠️ Ошибка кеширования: {e}")

            return response

        return wrapper
    return decorator
