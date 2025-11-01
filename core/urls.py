from django.urls import path
from core.views_cache_admin import cache_status_view, cache_status_json

app_name = 'core'

urlpatterns = [
    path("cache-status/", cache_status_view, name="cache_status"),
    path("cache-status/json/", cache_status_json, name="cache_status_json"),
]
