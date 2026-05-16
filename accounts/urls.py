
from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'accounts'

urlpatterns = [
    # Редирект с пустого пути на логин
    #path('', views.login_view, name='login'),
    #path('', lambda request: redirect('accounts:login'), name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/edit-role/', views.user_edit_role_view, name='user_edit_role'),
]
