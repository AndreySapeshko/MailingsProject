"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mailings.views.home_view import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('recipients/', include('recipients.urls', namespace='recipients')),
    path('mailings/', include('mailings.urls', namespace='mailings')),
    path('users/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
