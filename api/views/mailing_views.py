from django.core.cache import cache
from rest_framework import viewsets
from mailings.models import Mailing
from api.serializers.mailing_serializers import MailingSerializer
from api.mixins import BaseCachedViewSetMixin
from api.utils.cache import cache_response

class MailingViewSet(BaseCachedViewSetMixin, viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
