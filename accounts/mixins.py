from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin для CBV - только администраторы"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
    
    def handle_no_permission(self):
        raise PermissionDenied("Только для администраторов")

class ManagerRequiredMixin(UserPassesTestMixin):
    """Mixin для CBV - менеджеры и администраторы"""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_admin or self.request.user.is_manager
        )
    
    def handle_no_permission(self):
        raise PermissionDenied("Только для менеджеров и администраторов")

class LoginRequiredMixin(UserPassesTestMixin):
    """Mixin для авторизованных пользователей"""
    def test_func(self):
        return self.request.user.is_authenticated
    
    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect('accounts:login')