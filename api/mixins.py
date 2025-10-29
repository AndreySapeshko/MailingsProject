from django.core.cache import cache
from api.utils.cache import cache_response
from api.permissions import RoleBasedAccessPermission

class BaseCachedViewSetMixin:
    """
    Базовый миксин для API ViewSet-ов:
    - Кеширование list и retrieve
    - Очистка кеша при изменениях
    - Автоматическая фильтрация по пользователю
    """
    permission_classes = [RoleBasedAccessPermission]
    cache_prefix = "api"

    def clear_api_cache(self):
        """Удаляет все ключи кеша, относящиеся к API"""
        keys = cache.keys(f"{self.cache_prefix}:*")
        if keys:
            cache.delete_many(keys)
            print(f"🧹 Кеш API очищен ({len(keys)} ключей)")

    def perform_create(self, serializer):
        self.clear_api_cache()
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.clear_api_cache()
        serializer.save()

    def perform_destroy(self, instance):
        self.clear_api_cache()
        return super().perform_destroy(instance)

    def get_queryset(self):
        """Ограничивает выборку по пользователю, если он не менеджер/админ"""
        user = self.request.user
        qs = super().get_queryset()
        if not (user.is_superuser or user.role in ['manager', 'admin']):
            qs = qs.filter(user=user)
        return qs

    @cache_response(timeout=120)
    def list(self, request, *args, **kwargs):
        """Кеширование списка"""
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=300)
    def retrieve(self, request, *args, **kwargs):
        """Кеширование детального просмотра"""
        return super().retrieve(request, *args, **kwargs)
