from django.contrib import admin
from products.models import ProductsCategory, Product

# Register your models here.
admin.site.register(ProductsCategory)
admin.site.register(Product)
