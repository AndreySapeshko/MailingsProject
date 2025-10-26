from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False, verbose_name='Менеджер рассылок')

    def __str__(self):
        return self.username or self.email
