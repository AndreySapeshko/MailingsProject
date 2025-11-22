from django.utils.decorators import method_decorator
from core.decorators import universal_cache


class CachedViewMixin:
    """
    Универсальный миксин для кеширования CBV:
    - Работает с любыми классами, где есть метод get()
    - Поддерживает prefix и timeout (через атрибуты)
    """

    cache_prefix = "page"      # дефолтный префикс для кеша
    cache_timeout = 300        # дефолтный TTL (в секундах)

    @classmethod
    def as_view(cls, **initkwargs):
        """Переопределяем as_view, чтобы автоматически навешивать декоратор"""
        view = super().as_view(**initkwargs)

        # Получаем настройки из класса (если переопределены)
        prefix = cls.cache_prefix
        timeout = getattr(cls, "cache_timeout", 300)

        decorated_get = method_decorator(
            universal_cache(prefix=cls.cache_prefix, timeout=cls.cache_timeout)
        )(cls.get)

        cls.get = decorated_get
        return view
