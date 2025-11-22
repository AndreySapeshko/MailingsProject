from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Recipient
from api.serializers.recipient_serializers import RecipientSerializer
from api.mixins import BaseCachedViewSetMixin
from api.permissions import RoleBasedAccessPermission


class RecipientViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    """
        API endpoint for managing email recipients.

        - Только пользователь-владелец может изменять данные
        - Менеджер может только просматривать
        - Администратор имеет полный доступ
        """

    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
