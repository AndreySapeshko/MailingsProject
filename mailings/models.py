from django.conf import settings
from django.db import models
from recipients.models import Recipient
from django.utils import timezone
from django.core.mail import send_mail


class MailingLog(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='logs')
    recipient = models.ForeignKey('recipients.Recipient', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ('success', 'Успешно'),
        ('failed', 'Ошибка'),
    ])
    server_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mailing.name} → {self.recipient.email} [{self.status}]"


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
        ('completed', 'Завершена'),
        ('stopped', 'Остановлена')
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

    def send_now(self):
        """Отправка рассылки вручную"""

        sent_count = 0
        for recipient in self.recipients.all():
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    fail_silently=False,
                )
                MailingLog.objects.create(
                    mailing=self,
                    recipient=recipient,
                    status='success',
                    server_response='OK',
                )
                sent_count += 1
            except Exception as e:
                MailingLog.objects.create(
                    mailing=self,
                    recipient=recipient,
                    status='failed',
                    server_response=str(e),
                )
        self.status = 'completed'
        self.save(update_fields=['status'])
        return sent_count

    def launch(self):
        """Запуск рассылки"""

        self.status = 'launched'
        self.save(update_fields=['status'])

    def stop(self):
        """Остановка рассылки"""

        self.status = 'stopped'
        self.save(update_fields=['status'])

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка: {self.message.subject} ({self.user.username})"

