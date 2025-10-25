from django.urls import path
from mailings.views.message_views import (
    MessageListView, MessageCreateView,
    MessageUpdateView, MessageDeleteView
)
from mailings.views.mailing_views import (
    MailingListView, MailingCreateView,
    MailingUpdateView, MailingDeleteView,
)

app_name = 'mailings'

urlpatterns = [
    # message CRUD
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    # Mailings
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
