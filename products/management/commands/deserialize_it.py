from json import load
import os

from django.core.management.base import BaseCommand

from products.models import Product, ProductsCategory

JSON_PATH = 'products/fixtures'


def load_from_json(file_name):
    path = os.path.join(JSON_PATH, f'{file_name}.json')
    with open(path, 'r', encoding='utf-8') as infile:
        return load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories_list = load_from_json('its_categories')
        products_list = load_from_json('its_products')

        Product.objects.all().delete()
        ProductsCategory.objects.all().delete()
        print('Models cleaned')

        for category_item in categories_list:
            print(f"Adding category: {category_item['name']}")
            ProductsCategory.objects.create(**category_item)

        for product_item in products_list:
            print(f"Adding product: {product_item['name']}")
            category_name = product_item["category"]
            _category = ProductsCategory.objects.get(name=category_name)
            product_item['category'] = _category
            Product.objects.create(**product_item)

        print('All items deserialized.')
