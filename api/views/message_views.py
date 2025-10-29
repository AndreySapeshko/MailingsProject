from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Message
from api.serializers.message_serializers import MessageSerializer
from api.mixins import BaseCachedViewSetMixin
from api.utils.cache import cache_response


class MessageViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
