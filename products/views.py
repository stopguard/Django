from datetime import datetime

from django.shortcuts import render, get_object_or_404

from products.models import ProductsCategory, Product


# Create your views here.
# Controller-functions
def index(request):
    context = {
        'page_title': 'geekshop',
        'today': datetime.now(),
    }
    return render(request, 'index.html', context)


def products(request, cat_id=0):
    db_categories = ProductsCategory.objects.filter(is_active=True)
    title = 'geekshop - каталог'
    if cat_id == 0:
        db_products = Product.objects.filter(is_active=True, quantity__gt=0, category__is_active=True).order_by('price')
        category = {'name': 'все'}
    else:
        category = get_object_or_404(ProductsCategory, id=cat_id, is_active=True)
        db_products = Product.objects.filter(category_id=cat_id, is_active=True, quantity__gt=0).order_by('price')

    context = {
        'page_title': title,
        'today': datetime.now(),
        'category': category,
        'products': db_products,
        'categories': db_categories,
    }
    return render(request, 'products.html', context)
