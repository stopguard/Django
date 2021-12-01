from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from geekshop import settings
from products.models import ProductsCategory, Product


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductsCategory.objects.filter(is_active=True)
            cache.set(key, categories)
        return categories
    return ProductsCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductsCategory, id=pk, is_active=True)
            cache.set(key, category)
        return category
    return get_object_or_404(ProductsCategory, id=pk, is_active=True)


def get_products(cat_pk=0):
    if settings.LOW_CACHE:
        key = f'category_{cat_pk}_products'
        products = cache.get(key)
        if products is None:
            products = get_category(cat_pk).get_products().order_by('price') \
                if cat_pk \
                else Product.objects.select_related('category') \
                .filter(is_active=True, quantity__gt=0, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    products = get_category(cat_pk).get_products().order_by('price') \
        if cat_pk \
        else Product.objects.select_related('category') \
        .filter(is_active=True, quantity__gt=0, category__is_active=True).order_by('price')
    return products


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, id=pk, is_active=True, category__is_active=True)
            cache.set(key, product)
        return product
    return get_object_or_404(Product, id=pk, is_active=True, category__is_active=True)


def index(request):
    context = {
        'page_title': 'geekshop',
    }
    return render(request, 'index.html', context)


def products(request, cat_id=0):
    page_num = int(request.GET.get('page', 1))
    db_categories = get_categories()
    title = 'geekshop - каталог'
    if cat_id == 0:
        db_products = get_products()
    else:
        _ = get_category(cat_id)
        db_products = get_products(cat_id)

    # paginator
    products_pages = Paginator(db_products, 6)
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
        'category_pk': cat_id,
        'pages': page_list,
        'page_num': page_num,
        'products': db_products,
        'categories': db_categories,
    }
    return render(request, 'products.html', context)


def get_price(request, product_id):
    if request.is_ajax():
        product = get_product(product_id)
        price = product.price
        return JsonResponse({'status': True, 'price': price})
