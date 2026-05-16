from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin', password='test123', role='admin'
        )
        self.manager = User.objects.create_user(
            username='manager', password='test123', role='manager'
        )
        self.user = User.objects.create_user(
            username='user', password='test123', role='user'
        )
    
    def test_user_roles(self):
        """Тест ролей пользователей"""
        self.assertTrue(self.admin.is_admin)
        self.assertTrue(self.manager.is_manager)
        self.assertTrue(self.user.is_regular_user)
        
        self.assertFalse(self.admin.is_regular_user)
        self.assertFalse(self.manager.is_admin)
    
    def test_login(self):
        """Тест входа в систему"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'admin',
            'password': 'test123'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после входа
    
    def test_admin_access_to_user_list(self):
        """Тест доступа админа к списку пользователей"""
        self.client.login(username='admin', password='test123')
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 200)
        
        self.client.logout()
        self.client.login(username='user', password='test123')
        response = self.client.get(reverse('accounts:user_list'))
        self.assertEqual(response.status_code, 403)  # Доступ запрещён