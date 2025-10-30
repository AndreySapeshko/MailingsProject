from functools import wraps
from django.http import HttpResponse
from rest_framework.response import Response
from core.cache_utils import get_cache, set_cache
import inspect

def universal_cache(prefix="page", timeout=300):
    """
    Универсальный кеш-декоратор:
    - Работает и с DRF ViewSet, и с обычными Django CBV/FBV.
    - Формирует ключ по URL и пользователю.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # Определяем request независимо от типа view
            request = None
            for arg in args:
                if hasattr(arg, "META"):  # HttpRequest
                    request = arg
                    break
                if hasattr(arg, "request"):  # self.request
                    request = arg.request
                    break

            if not request:
                return view_func(*args, **kwargs)

            if request.method != "GET":
                return view_func(*args, **kwargs)

            user_id = getattr(request.user, "id", "anon")
            path = request.get_full_path()
            cached = get_cache(path, user_id, prefix)

            if cached:
                print(f"⚡ Кеш {prefix.upper()}: {path}")
                if inspect.isclass(type(args[0])) and hasattr(args[0], "get_serializer"):  # DRF
                    return Response(cached)
                return HttpResponse(cached)

            response = view_func(*args, **kwargs)
            data = None
            if isinstance(response, Response):
                response.render()
                data = response.data
            elif isinstance(response, HttpResponse):
                data = response.content

            if data:
                set_cache(path, user_id, data, prefix, timeout)
                print(f"🧠 Сохранен кеш {prefix.upper()}: {path}")

            return response

        return wrapper
    return decorator
