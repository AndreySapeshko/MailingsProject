import os

from django.core.cache import cache
from api.utils.cache import cache_response
from api.permissions import RoleBasedAccessPermission
from core.decorators import universal_cache


class BaseCachedViewSetMixin:
    """
    Базовый миксин для API ViewSet - ов:
    - Кеширование list и retrieve
    - Очистка кеша при изменениях
    - Автоматическая фильтрация по пользователю
    По умолчанию cache_prefix = "api", cache_timeout = 300 для
    изменения в наследнике передать в эти переменные необходимые значения.
    """

    permission_classes = [RoleBasedAccessPermission]
    cache_prefix = "api"
    cache_timeout = 300

    if os.environ.get("DISABLE_API_CACHE") == "1":
        cache_enabled = False
    else:
        cache_enabled = True

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not (user.is_superuser or user.role in ['manager', 'admin']):
            qs = qs.filter(user=user)
        return qs

    def list(self, request, *args, **kwargs):
        """Кеширование списка"""

        if not self.cache_enabled:
            return super().list(request, *args, **kwargs)
        prefix = self.cache_prefix or "api"
        timeout = self.cache_timeout or 300
        cached_func = universal_cache(prefix=prefix, timeout=timeout)(super().list)
        return cached_func(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Кеширование детального просмотра"""

        if not self.cache_enabled:
            return super().retrieve(request, *args, **kwargs)
        prefix = self.cache_prefix or "api"
        timeout = self.cache_timeout or 300
        cached_func = universal_cache(prefix=prefix, timeout=timeout)(super().retrieve)
        return cached_func(self, request, *args, **kwargs)
