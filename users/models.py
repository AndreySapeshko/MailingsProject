from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    class Roles(models.TextChoices):
        USER = 'user', 'Пользователь'
        MANAGER = 'manager', 'Менеджер'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name='Роль'
    )

    def is_manager(self):
        return self.role == self.Roles.MANAGER

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
