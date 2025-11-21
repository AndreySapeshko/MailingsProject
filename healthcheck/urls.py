from django.urls import path
from .views import health_live, health_ready

app_name = 'healthcheck'

urlpatterns = [
    path('live/', health_live, name='health-live'),
    path('ready/', health_ready, name='health-ready'),
]
