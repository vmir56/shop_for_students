from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Расширенная модель пользователя с ролью"""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MANAGER = 'manager', 'Менеджер'
        USER = 'user', 'Пользователь'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    
    # Добавляем related_name, чтобы избежать конфликта при смене Auth прежних users
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_groups',  # уникальное имя
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_permissions',  # уникальное имя
        related_query_name='accounts_user',
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    # Методы для проверки ролей
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
    
    @property
    def is_regular_user(self):
        return self.role == self.Role.USER
    
    def has_project_permission(self, action='view'):
        """Проверка прав на проекты"""
        if self.is_admin:
            return True
        if action == 'view':
            return True
        if action in ['create', 'update', 'delete']:
            return self.is_admin
        return False
    
    def has_task_permission(self, action='view'):
        """Проверка прав на задачи"""
        if self.is_admin:
            return True
        if action == 'view':
            return True
        if action in ['create', 'update']:
            return self.is_manager or self.is_admin
        if action == 'delete':
            return self.is_admin
        if action == 'complete':
            return True
        return False