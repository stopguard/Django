from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from adminapp.forms import ShopUserEditForm, CategoryForm, ProductForm
from authapp.forms import ShopUserRegisterForm
from basketapp.models import Basket
from products.models import Product, ProductsCategory


class SuOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ContextMixin:
    today = datetime.now()
    page_title = None
    basket = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            basket=self.basket,
            page_title=self.page_title,
            today=self.today
        )
        return context


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    context = {
        'page_title': 'Администрирование',
    }
    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda user: user.is_superuser)
def users(request):
    users_list = get_user_model().objects.all()
    context = {
        'page_title': 'Управление - пользователи',
        'users': users_list
    }
    return render(request, 'adminapp/users/users.html', context)


# @user_passes_test(lambda user: user.is_superuser)
# def user_edit(request, uid):
#     selected_user = get_object_or_404(get_user_model(), id=uid)
#     if request.method == 'POST':
#         profile_form = ShopUserEditForm(data=request.POST, files=request.FILES, instance=user)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Профиль отредактирован!')
#     else:
#         profile_form = ShopUserEditForm(instance=selected_user)
#     basket = Basket.objects.filter(user=selected_user)
#     available_products = Product.objects.all()
#     context = {
#         'page_title': f'Управление пользователем {selected_user.username}',
#         'today': datetime.now(),
#         'profile_form': profile_form,
#         'basket': basket,
#         'selected_user': selected_user,
#         'products': available_products,
#     }
#     return render(request, 'adminapp/users/profile.html', context)


class UserEdit(SuOnlyMixin, ContextMixin, UpdateView):
    model = get_user_model()
    form_class = ShopUserEditForm
    success_url = reverse_lazy('auth_admin:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'Управление пользователем {self.object.username}'
        basket = Basket.objects.filter(user_id=self.object.pk)
        context.update(
            basket=basket,
            page_title=page_title,
        )
        return context


@user_passes_test(lambda user: user.is_superuser)
def user_delete(request, uid):
    selected_user = get_object_or_404(get_user_model(), id=uid)
    if not selected_user.is_active or request.method == 'POST':
        if selected_user.is_active:
            selected_user.is_active = False
            selected_user.save()
        messages.add_message(request, messages.SUCCESS, f'Пользователь {selected_user.username} удалён!')
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'page_title': f'Удаление пользователя {selected_user.username}',
        'user_to_del': selected_user,
    }
    return render(request, 'adminapp/users/delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_restore(request, uid):
    selected_user = get_object_or_404(get_user_model(), id=uid)
    if selected_user.is_active or request.method == 'POST':
        if not selected_user.is_active:
            selected_user.is_active = True
            selected_user.save()
        messages.add_message(request, messages.SUCCESS, f'Пользователь {selected_user.username} восстановлен!')
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'page_title': f'Восстановление пользователя {selected_user.username}',
        'user_to_restore': selected_user,
    }
    return render(request, 'adminapp/users/restore.html', context)


@user_passes_test(lambda user: user.is_superuser)
def user_create(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.add_message(request, messages.SUCCESS, 'Пользователь создан!')
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'page_title': 'Создание пользователя',
        'register_form': register_form,
    }
    return render(request, 'adminapp/users/create.html', context)


@user_passes_test(lambda user: user.is_superuser)
def show_products(request):
    if request.is_ajax():
        products_all = Product.objects.all().order_by('name')
        context = {'products': products_all}
        products_all_html = render_to_string('adminapp/includes/add_to_basket.html', context=context, request=request)
        return JsonResponse({'status': True, 'products_all_html': products_all_html})


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     all_categories = ProductsCategory.objects.all()
#     context = {
#         'page_title': 'Управление - категории товаров',
#         'all_categories': all_categories,
#         'today': datetime.now(),
#     }
#     return render(request, 'adminapp/categories/templates/products/categories.html', context)


class Categories(SuOnlyMixin, ContextMixin, ListView):
    model = ProductsCategory
    page_title = 'Управление - категории товаров'


# @user_passes_test(lambda user: user.is_superuser)
# def category_edit(request, cat_id):
#     category = get_object_or_404(ProductsCategory, id=cat_id)
#     if request.method == 'POST':
#         form = CategoryForm(data=request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Категория {category.name} отредактирована!')
#     else:
#         form = CategoryForm(instance=category)
#     context = {
#         'page_title': f'Управление категорией {category.name}',
#         'today': datetime.now(),
#         'form': form,
#         'category': category,
#     }
#     return render(request, 'adminapp/categories/edit.html', context)


class CategoryEdit(SuOnlyMixin, ContextMixin, UpdateView):
    model = ProductsCategory
    form_class = CategoryForm
    success_url = reverse_lazy('auth_admin:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Управление категорией {self.object.name}'
        return context


# @user_passes_test(lambda user: user.is_superuser)
# def category_delete(request, cat_id):
#     category = get_object_or_404(ProductsCategory, id=cat_id)
#     if not category.is_active or request.method == 'POST':
#         if category.is_active:
#             category.is_active = False
#             category.save()
#         messages.success(request, f'Категория {category.name} удалёна!')
#         return HttpResponseRedirect(reverse('auth_admin:categories'))
#     context = {
#         'page_title': f'Удаление категории {category.name}',
#         'category_to_del': category,
#         'today': datetime.now(),
#     }
#     return render(request, 'adminapp/categories/templates/products/delete.html', context)


class CategoryDelete(SuOnlyMixin, ContextMixin, DeleteView):
    model = ProductsCategory
    success_url = reverse_lazy('auth_admin:categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Удаление категории {self.object.name}'
        return context


@user_passes_test(lambda user: user.is_superuser)
def products(request):
    products_list = Product.objects.all()
    context = {
        'page_title': 'Управление - продукты',
        'products': products_list,
    }
    return render(request, 'adminapp/products/products.html', context)


@user_passes_test(lambda user: user.is_superuser)
def category_restore(request, cat_id):
    category = get_object_or_404(ProductsCategory, id=cat_id)
    if category.is_active or request.method == 'POST':
        if not category.is_active:
            category.is_active = True
            category.save()
        messages.add_message(request, messages.SUCCESS, f'Категория {category.name} восстановлена!')
        return HttpResponseRedirect(reverse('auth_admin:categories'))
    context = {
        'page_title': f'Восстановление категории {category.name}',
        'category_to_restore': category,
    }
    return render(request, 'adminapp/categories/restore.html', context)


# @user_passes_test(lambda user: user.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = CategoryForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Категория создана!')
#             return HttpResponseRedirect(reverse('auth_admin:categories'))
#     else:
#         form = CategoryForm()
#     context = {
#         'page_title': 'Создание категории',
#         'today': datetime.now(),
#         'form': form,
#     }
#     return render(request, 'adminapp/categories/create.html', context)


class CategoryCreate(SuOnlyMixin, ContextMixin, CreateView):
    model = ProductsCategory
    form_class = CategoryForm
    success_url = reverse_lazy('auth_admin:categories')
    page_title = 'Создание категории',


@user_passes_test(lambda user: user.is_superuser)
def products(request):
    products_list = Product.objects.all()
    context = {
        'page_title': 'Управление - продукты',
        'products': products_list,
    }
    return render(request, 'adminapp/products/products.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_edit(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Продукт отредактирован!')
    else:
        form = ProductForm(instance=product)
    context = {
        'page_title': f'Управление продуктом {product.name}',
        'form': form,
        'product': product,
    }
    return render(request, 'adminapp/products/edit.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_delete(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if not product.is_active or request.method == 'POST':
        if product.is_active:
            product.is_active = False
            product.save()
        messages.add_message(request, messages.SUCCESS, 'Продукт удалён!')
        return HttpResponseRedirect(reverse('auth_admin:products'))
    context = {
        'page_title': f'Удаление продукта {product.name}',
        'product_to_del': product,
    }
    return render(request, 'adminapp/products/delete.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_restore(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    if product.is_active or request.method == 'POST':
        if not product.is_active:
            product.is_active = True
            product.save()
        messages.add_message(request, messages.SUCCESS, 'Продукт восстановлен!')
        return HttpResponseRedirect(reverse('auth_admin:products'))
    context = {
        'page_title': f'Восстановление продукта {product.name}',
        'product_to_restore': product,
    }
    return render(request, 'adminapp/products/restore.html', context)


@user_passes_test(lambda user: user.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Продукт создан!')
            return HttpResponseRedirect(reverse('auth_admin:products'))
    else:
        form = ProductForm()
    context = {
        'page_title': 'Создание продукта',
        'form': form,
    }
    return render(request, 'adminapp/products/create.html', context)
