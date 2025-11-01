from django.contrib import admin
from .models import Mailing, Message, MailingLog
from recipients.models import Recipient

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'status', 'date_first_dispatch', 'dispatch_end_date')
    list_filter = ('status', 'periodicity')
    search_fields = ('name', 'user__username')
    ordering = ('-date_first_dispatch',)
    date_hierarchy = 'date_first_dispatch'
    autocomplete_fields = ('user', 'recipients', 'message')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'user')
    search_fields = ('subject', 'body')
    autocomplete_fields = ('user',)

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'user')
    search_fields = ('email', 'name')
    list_filter = ('user',)

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'recipient', 'timestamp', 'status')
    list_filter = ('status', 'timestamp')
    search_fields = ('mailing__name', 'recipient__email')
    date_hierarchy = 'timestamp'
