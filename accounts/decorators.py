from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    """Декоратор для проверки роли пользователя"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                pass
                # return redirect('accounts:login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'У вас нет доступа к этой странице.')
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    """Только для администраторов"""
    return role_required(['admin'])(view_func)

def manager_required(view_func):
    """Для менеджеров и администраторов"""
    return role_required(['admin', 'manager'])(view_func)

def user_required(view_func):
    """Для всех авторизованных пользователей"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper