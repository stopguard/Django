"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('users/', adminapp.users, name='users'),
    path('users/profile/<int:pk>/', adminapp.UserEdit.as_view(), name='user_edit'),
    path('users/delete/<int:uid>/', adminapp.user_delete, name='user_delete'),
    path('users/restore/<int:uid>/', adminapp.user_restore, name='user_restore'),
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/profile/show_products/', adminapp.show_products),           # AJAX
    path('categories/', adminapp.Categories.as_view(), name='categories'),
    path('categories/edit/<int:pk>/', adminapp.CategoryEdit.as_view(), name='category_edit'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDelete.as_view(), name='category_delete'),
    path('categories/restore/<int:cat_id>/', adminapp.category_restore, name='category_restore'),
    path('categories/create/', adminapp.CategoryCreate.as_view(), name='category_create'),
    path('products/', adminapp.products, name='products'),
    path('products/edit/<int:prod_id>/', adminapp.product_edit, name='product_edit'),
    path('products/delete/<int:prod_id>/', adminapp.product_delete, name='product_delete'),
    path('products/restore/<int:prod_id>/', adminapp.product_restore, name='product_restore'),
    path('products/create/', adminapp.product_create, name='product_create'),
]
