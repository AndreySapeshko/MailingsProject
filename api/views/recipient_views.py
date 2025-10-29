from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Recipient
from api.serializers.recipient_serializers import RecipientSerializer
from api.permissions import RoleBasedAccessPermission
from api.utils.cache import cache_response


class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
    permission_classes = [RoleBasedAccessPermission]

    def clear_api_cache(prefix="api"):
        keys = cache.keys(f"{prefix}:*")
        cache.delete_many(keys)
        print(f"🧹 Кеш API очищен ({len(keys)} ключей)")

    def perform_create(self, serializer):
        self.clear_api_cache()
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role in ['manager', 'admin']:
            return Recipient.objects.all()
        return Recipient.objects.filter(user=user)

    @cache_response(timeout=120)  # ✅ кэшируем список на 2 минуты
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=300)  # ✅ кэшируем детальный просмотр на 5 минут
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)