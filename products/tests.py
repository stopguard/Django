from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from products.models import ProductsCategory, Product


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


class TestProductModel(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = ProductsCategory.objects.create(name="стулья")
        cls.product_1 = Product.objects.create(name="стул 1",
                                               category=category,
                                               price=1999.5,
                                               quantity=150)

        cls.product_2 = Product.objects.create(name="стул 2",
                                               category=category,
                                               price=2998.1,
                                               quantity=125,
                                               is_active=False)

        cls.product_3 = Product.objects.create(name="стул 3",
                                               category=category,
                                               price=998.1,
                                               quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(str(product_1), 'стул 1 / стулья')
        self.assertEqual(str(product_2), 'стул 2 / стулья')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="стул 1")
        product_3 = Product.objects.get(name="стул 3")
        products = product_1.category.get_products()

        self.assertEqual(list(products), [product_1, product_3])
