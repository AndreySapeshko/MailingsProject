from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ManagerRequiredMixin(UserPassesTestMixin):
    """Доступ только менеджерам и администраторам"""

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_manager() or self.request.user.is_superuser
        )

class OwnerOrManagerMixin(UserPassesTestMixin):
    """Доступ только владельцу объекта или менеджеру"""
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        print(f"DEBUG: user={user}, role={user.role}, is_superuser={user.is_superuser}")
        return (
            obj.user == user or
            user.is_manager() or
            user.is_superuser
        )


class AccessByRoleMixin(UserPassesTestMixin):
    """
    Универсальный миксин для контроля доступа по ролям.
    Поддерживает:
      - индивидуальные настройки в модели (access_roles)
      - глобальные правила в settings.ROLE_ACCESS
    """

    raise_exception = True  # возвращать 403 при отсутствии прав

    def get_allowed_roles(self, obj_or_model):
        """
        Определяет, какие роли имеют доступ к объекту или модели.
        Приоритет: model.access_roles > settings.ROLE_ACCESS
        """
        # Проверяем наличие access_roles у модели
        allowed_roles = getattr(obj_or_model, "access_roles", None)
        if allowed_roles is not None:
            return allowed_roles

        # Если нет — ищем глобальное правило по app_label
        app_label = getattr(obj_or_model._meta, "app_label", None)
        return getattr(settings, "ROLE_ACCESS", {}).get(app_label, [])

    def test_func(self):
        """Проверка прав для Detail/Update/DeleteView"""
        user = self.request.user

        # Суперпользователь — всегда имеет доступ
        if user.is_superuser:
            return True

        # Для вьюшек с объектом (Detail/Update/Delete)
        if hasattr(self, "get_object"):
            try:
                obj = self.get_object()
            except Exception:
                return False

            allowed_roles = self.get_allowed_roles(obj)
            if user.role in allowed_roles:
                return True

            if isinstance(obj, User) and obj == user:
                return True

            if hasattr(obj, "user") and obj.user == user:
                return True

            # Если не владелец и роль не подходит — отказ
            return False

        # Для ListView (без объекта) — просто проверка авторизации
        return True

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Админ видит всё
        if user.is_superuser:
            return qs

        # Проверяем разрешённые роли по app_label
        allowed_roles = self.get_allowed_roles(qs.model)
        if user.role in allowed_roles:
            return qs

        # Владелец видит только свои объекты
        if hasattr(qs.model, "user"):
            return qs.filter(user=user)

        return qs.none()

