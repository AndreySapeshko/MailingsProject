from django.db import models
from django.conf import settings


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='email')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipients'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return f"{self.name} <{self.email}>"
