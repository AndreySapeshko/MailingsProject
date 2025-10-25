from django.conf import settings
from django.db import models
from recipients.models import Recipient


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена')
    ]
    PERIODICITY_CHOICES = [
        ('once', 'Один раз'),
        ('daily', 'Каждый день'),
        ('weekly', 'Раз в неделю'),
    ]
    name = models.CharField(max_length=100, verbose_name='Название')
    date_first_dispatch = models.DateTimeField(verbose_name='Дата первой отправки')
    dispatch_end_date = models.DateTimeField(verbose_name='Дата окончания отправки')
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES, default='once',
                                   verbose_name='Периодичность')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings'
    )
    recipients = models.ManyToManyField(Recipient, related_name='mailings')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка: {self.message.subject} ({self.user.username})"

