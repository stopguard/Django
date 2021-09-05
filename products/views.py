from django.shortcuts import render
from datetime import datetime
from products.models import ProductsCategory, Product


# Create your views here.
# Controller-functions
def index(request):
    context = {
        'page_title': 'geekshop',
        'today': datetime.now(),
    }
    return render(request, 'index.html', context)


def products(request):
    db_categories = ProductsCategory.objects.all()
    db_products = Product.objects.all()
    context = {
        'page_title': 'geekshop - каталог',
        'today': datetime.now(),
        'products': db_products,
        'categories': db_categories,
    }
    return render(request, 'products.html', context)
