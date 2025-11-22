from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Mailing
from api.serializers.mailing_serializers import MailingSerializer
from api.mixins import BaseCachedViewSetMixin
from api.permissions import RoleBasedAccessPermission
from core.decorators import universal_cache

class MailingViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    """
        API endpoint for managing email mailings.

        - Только пользователь-владелец может изменять данные
        - Менеджер может только просматривать
        - Администратор имеет полный доступ
        """

    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
