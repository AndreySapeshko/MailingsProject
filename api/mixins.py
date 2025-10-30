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

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if not (user.is_superuser or user.role in ['manager', 'admin']):
            qs = qs.filter(user=user)
        return qs

    def list(self, request, *args, **kwargs):
        """Кеширование списка"""
        prefix = self.cache_prefix or "api"
        timeout = self.cache_timeout or 300
        cached_func = universal_cache(prefix=prefix, timeout=timeout)(super().list)
        return cached_func(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Кеширование детального просмотра"""
        prefix = self.cache_prefix or "api"
        timeout = self.cache_timeout or 300
        cached_func = universal_cache(prefix=prefix, timeout=timeout)(super().retrieve)
        return cached_func(self, request, *args, **kwargs)
