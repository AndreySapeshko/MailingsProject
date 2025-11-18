import logging
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.conf import settings
from django.contrib.auth import get_user_model
from functools import lru_cache

logger = logging.getLogger('django')

User = get_user_model()


class RoleBasedAccessPermission(BasePermission):
    """
    Permission с кешированием ролей и прав.
    Поведение:
      - суперпользователь: полный доступ;
      - разрешённые роли по settings.ROLE_ACCESS;
      - просмотр для allow_view_only_roles;
      - владельцы могут изменять свои данные.
    """

    # Кешируем данные о ролях и разрешениях на уровне класса
    @staticmethod
    @lru_cache(maxsize=None)
    def get_allowed_roles(app_label):
        """Возвращает роли, разрешённые для данного приложения"""
        role_access = getattr(settings, "ROLE_ACCESS", {})
        return role_access.get(app_label, [])

    @staticmethod
    @lru_cache(maxsize=None)
    def get_view_only_roles():
        """Возвращает роли, которым разрешён только просмотр"""
        return getattr(settings, "ALLOW_VIEW_ONLY_ROLES", [])

    def has_permission(self, request, view):
        user = request.user

        # 1 Только авторизованные пользователи
        if not user.is_authenticated:
            return False

        # 2 Суперпользователь — всегда да
        if user.is_superuser:
            return True

        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if user.role == "admin":
                return True
            if user.role == "user":
                return True  # проверка владения в has_object_permission
            return False

        if request.method in SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # 1 Суперпользователь — полный доступ
        if user.is_superuser:
            return True

        # 2 Разрешён просмотр для read-only ролей
        if request.method in SAFE_METHODS and user.role in self.get_view_only_roles():
            return True

        # 3 Владельцы могут редактировать свои объекты
        if isinstance(obj, User) and obj == user:
            return True
        if hasattr(obj, "user") and obj.user == user:
            return True

        # 4 Проверка разрешённых ролей
        model = getattr(view, "queryset", None).model
        app_label = model._meta.app_label if model else None
        allowed_roles = self.get_allowed_roles(app_label)
        logger.info('Роль пользователя не подошла для доступа')
        return user.role in allowed_roles
