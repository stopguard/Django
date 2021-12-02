from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from products.models import ProductsCategory


class TestProductsSmoke(TestCase):
    fixtures = ['products.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_product_urls(self):
        response = self.client.get(reverse('products:index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('products:products'))
        self.assertEqual(response.status_code, 200)

    def test_category_urls(self):
        response = self.client.get(reverse('products:category',
                                           kwargs={'cat_id': 0}))
        self.assertEqual(response.status_code, 200)

        for category in ProductsCategory.objects.filter(is_active=True):
            response = self.client.get(reverse('products:category', kwargs={'cat_id': category.pk}))
            self.assertEqual(response.status_code, 200)
