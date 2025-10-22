from django.conf import settings
from django.db import models


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipient'
    )

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Message(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message'
    )

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена')
    ]
    name = models.CharField(max_length=100, verbose_name='Название')
    date_first_dispatch = models.DateTimeField(verbose_name='Дата первой отправки')
    dispatch_end_date = models.DateTimeField(verbose_name='Дата окончания отправки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailing'
    )
    recipients = models.ManyToManyField(Recipient, related_name='mailings')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')

    def __str__(self):
        return f"Рассылка: {self.message.subject} ({self.user.username})"

