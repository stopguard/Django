from json import dump
import os

from django.core.management.base import BaseCommand

from products.models import Product, ProductsCategory

JSON_PATH = 'products/fixtures'


def save_to_json(data: list, file_name: str):
    path = os.path.join(JSON_PATH, f'{file_name}.json')
    with open(path, 'w', encoding='utf-8') as infile:
        dump(data, infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories_query = ProductsCategory.objects.all()
        products_query = Product.objects.all()
        categories_list, products_list = [], []
        print('Prepare: OK')
        for category in categories_query:
            print(f"Read category: {category.name}")
            categories_list.append({
                'name': category.name,
                'description': category.description
            })

        for product in products_query:
            print(f"Read product: {product.name}")
            products_list.append({
                'name': product.name,
                'image': str(product.image),
                'description': product.description,
                'price': str(product.price),
                'quantity': product.quantity,
                'category': categories_query.filter(id=product.category_id)[0].name
            })

        save_to_json(categories_list, 'its_categories')
        print('Categories serialized.')
        save_to_json(products_list, 'its_products')
        print('Products serialized.\nAll items serialized.')
