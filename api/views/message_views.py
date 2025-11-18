from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Message
from api.serializers.message_serializers import MessageSerializer
from api.mixins import BaseCachedViewSetMixin
from api.permissions import RoleBasedAccessPermission


class MessageViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    """
        API endpoint for managing email messages.

        - Только пользователь-владелец может изменять данные
        - Менеджер может только просматривать
        - Администратор имеет полный доступ
        """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
