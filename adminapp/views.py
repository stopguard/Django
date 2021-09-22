from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from adminapp.forms import ShopUserEditForm, CategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from basketapp.models import Basket
from products.models import Product, ProductsCategory


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    context = {
        'page_title': 'Администрирование',
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda user: user.is_superuser)
def users(request):
    users_list = get_user_model().objects.all()
    context = {
        'page_title': 'Управление - пользователи',
        'users': users_list,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/users/users.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_edit(request, uid):
    user = get_object_or_404(get_user_model(), id=uid)
    if request.method == 'POST':
        profile_form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Профиль отредактирован!')
    else:
        profile_form = ShopUserEditForm(instance=user)
    basket = Basket.objects.filter(user=user)
    available_products = Product.objects.all()
    context = {
        'page_title': f'Управление пользователем {user.username}',
        'today': datetime.now(),
        'profile_form': profile_form,
        'basket': basket,
        'user': user,
        'products': available_products,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/users/profile.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, uid):
    user = get_object_or_404(get_user_model(), id=uid)
    if not user.is_active or request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
        messages.success(request, f'Пользователь {user.username} удалён!')
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'page_title': f'Удаление пользователя {user.username}',
        'user_to_del': user,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/users/delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_restore(request, uid):
    user = get_object_or_404(get_user_model(), id=uid)
    if user.is_active or request.method == 'POST':
        if not user.is_active:
            user.is_active = True
            user.save()
        messages.success(request, f'Пользователь {user.username} восстановлен!')
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'page_title': f'Восстановление пользователя {user.username}',
        'user_to_restore': user,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/users/restore.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_create(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Пользователь создан!')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'page_title': 'Создание пользователя',
        'today': datetime.now(),
        'register_form': register_form,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/users/create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def show_products(request):
    if request.is_ajax():
        products_all = Product.objects.all().order_by('name')
        context = {'products': products_all}
        products_all_html = render_to_string('adminapp/includes/add_to_basket.html', context=context, request=request)
        return JsonResponse({'status': True, 'products_all_html': products_all_html})


@user_passes_test(lambda user: user.is_superuser)
def categories(request):
    all_categories = ProductsCategory.objects.all()
    context = {
        'page_title': 'Управление - категории товаров',
        'all_categories': all_categories,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/categories/categories.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_edit(request, cat_id):
    category = get_object_or_404(ProductsCategory, id=cat_id)
    if request.method == 'POST':
        form = CategoryForm(data=request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Категория {category.name} отредактирована!')
    else:
        form = CategoryForm(instance=category)
    context = {
        'page_title': f'Управление категорией {category.name}',
        'today': datetime.now(),
        'form': form,
        'category': category,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/categories/edit.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_delete(request, cat_id):
    category = get_object_or_404(ProductsCategory, id=cat_id)
    if not category.is_active or request.method == 'POST':
        if category.is_active:
            category.is_active = False
            category.save()
        messages.success(request, f'Категория {category.name} удалёна!')
        return HttpResponseRedirect(reverse('auth_admin:categories'))
    context = {
        'page_title': f'Удаление категории {category.name}',
        'category_to_del': category,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/categories/delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_restore(request, cat_id):
    category = get_object_or_404(ProductsCategory, id=cat_id)
    if category.is_active or request.method == 'POST':
        if not category.is_active:
            category.is_active = True
            category.save()
        messages.success(request, f'Категория {category.name} восстановлена!')
        return HttpResponseRedirect(reverse('auth_admin:categories'))
    context = {
        'page_title': f'Восстановление категории {category.name}',
        'category_to_restore': category,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/categories/restore.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория создана!')
            return HttpResponseRedirect(reverse('auth_admin:categories'))
    else:
        form = CategoryForm()
    context = {
        'page_title': 'Создание категории',
        'today': datetime.now(),
        'form': form,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/categories/create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def products(request):
    products_list = Product.objects.all()
    context = {
        'page_title': 'Управление - продукты',
        'products': products_list,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/products/products.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_edit(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт отредактирован!')
    else:
        form = ProductForm(instance=product)
    context = {
        'page_title': f'Управление продуктом {product.name}',
        'today': datetime.now(),
        'form': form,
        'product': product,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/products/edit.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if not product.is_active or request.method == 'POST':
        if product.is_active:
            product.is_active = False
            product.save()
        messages.success(request, 'Продукт удалён!')
        return HttpResponseRedirect(reverse('auth_admin:products'))
    context = {
        'page_title': f'Удаление продукта {product.name}',
        'product_to_del': product,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/products/delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_restore(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if product.is_active or request.method == 'POST':
        if not product.is_active:
            product.is_active = True
            product.save()
        messages.success(request, 'Продукт восстановлен!')
        return HttpResponseRedirect(reverse('auth_admin:products'))
    context = {
        'page_title': f'Восстановление продукта {product.name}',
        'product_to_restore': product,
        'today': datetime.now(),
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/products/restore.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Продукт создан!')
            return HttpResponseRedirect(reverse('auth_admin:products'))
    else:
        form = ProductForm()
    context = {
        'page_title': 'Создание продукта',
        'today': datetime.now(),
        'form': form,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'adminapp/products/create.html', context)
