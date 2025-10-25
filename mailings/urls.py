from django.urls import path
from mailings.views.message_views import (
    MessageListView, MessageCreateView,
    MessageUpdateView, MessageDeleteView
)

app_name = 'mailings'

urlpatterns = [
    # message CRUD
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
