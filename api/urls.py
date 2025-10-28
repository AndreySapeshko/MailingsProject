from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.mailing_views import MailingViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'mailings', MailingViewSet, basename='mailing')

urlpatterns = [
    path('', include(router.urls)),
]
