from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.mailing_views import MailingViewSet
from api.views.message_views import MessageViewSet
from api.views.recipient_views import RecipientViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'mailings', MailingViewSet, basename='mailing')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'recipients', RecipientViewSet, basename='recipient')

urlpatterns = [
    path('', include(router.urls)),
]
