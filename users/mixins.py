from django.contrib.auth.mixins import UserPassesTestMixin

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
        return (
            obj.user == user or
            user.is_manager() or
            user.is_superuser
        )
