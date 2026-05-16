from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, LoginForm
from .decorators import role_required, admin_required

def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('store:catalog')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('store:catalog')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Вход в систему"""
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'С возвращением, {username}!')
                return redirect('store:catalog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """Профиль пользователя"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@admin_required
def user_list_view(request):
    """Список пользователей (только для админов)"""
    from .models import User
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@admin_required
def user_edit_role_view(request, user_id):
    """Редактирование роли пользователя (только для админов)"""
    from .models import User
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        user.role = new_role
        user.save()
        messages.success(request, f'Роль пользователя {user.username} изменена на {user.get_role_display()}')
        return redirect('accounts:user_list')
    
    return render(request, 'accounts/user_edit_role.html', {'user': user})