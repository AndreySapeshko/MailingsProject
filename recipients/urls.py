from django.urls import path
from . import views

app_name = 'recipients'

urlpatterns = [
    path('', views.RecipientListView.as_view(), name='list'),
    path('create/', views.RecipientCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.RecipientUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.RecipientDeleteView.as_view(), name='delete'),
]