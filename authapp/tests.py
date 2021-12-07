from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from authapp.models import ShopUser


class TestAuthUser(TestCase):
    fixtures = ['products.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.su = ShopUser.objects.create_superuser('rasras', 'rasras@dva.tri', '12345678')
        cls.usr = ShopUser.objects.create_user('dvadva', 'dvadva@dva.tri', '87654321')

    def test_login(self):
        response = self.client.get(reverse('products:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Выйти', status_code=200)

        self.client.post(reverse('auth:login'),
                         data={'username': 'rasras', 'password': '12345678'})
        response = self.client.get(reverse('products:index'))
        self.assertEqual(self.su, response.context['user'])
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        response = self.client.get(reverse('auth:profile'))
        self.assertEqual('/auth/login/?next=/auth/profile/', response.url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username='rasras', password='12345678')
        response = self.client.get(reverse('auth:profile'))
        self.assertEqual(response.status_code, 200)
