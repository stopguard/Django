from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    page_num = int(request.GET.get('page', 1))
    db_categories = ProductsCategory.objects.filter(is_active=True)
    title = 'geekshop - каталог'
    if cat_id == 0:
        db_products = Product.objects.filter(is_active=True, quantity__gt=0, category__is_active=True).order_by('price')
        category = {'name': 'все', 'pk': 0}
    else:
        category = get_object_or_404(ProductsCategory, id=cat_id, is_active=True)
        db_products = Product.objects.filter(category_id=cat_id, is_active=True, quantity__gt=0).order_by('price')

    # paginator
    products_pages = Paginator(db_products, 3)
    try:
        db_products = products_pages.page(page_num)
    except PageNotAnInteger:
        db_products = products_pages.page(1)
    except EmptyPage:
        db_products = products_pages.page(products_pages.num_pages)
    # paginator
    page_list = list(range(1, products_pages.num_pages + 1))
    context = {
        'page_title': title,
        'today': datetime.now(),
        'category': category,
        'pages': page_list,
        'page_num': page_num,
        'products': db_products,
        'categories': db_categories,
    }
    return render(request, 'products.html', context)
