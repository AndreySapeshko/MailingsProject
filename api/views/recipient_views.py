from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Recipient
from api.serializers.recipient_serializers import RecipientSerializer
from api.mixins import BaseCachedViewSetMixin
from api.permissions import RoleBasedAccessPermission


class RecipientViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
