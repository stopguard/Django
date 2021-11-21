from django.urls import path
import products.views as products

app_name = 'products'

urlpatterns = [
    path('', products.index, name='index'),
    path('products/', products.products, name='products'),
    path('category/<int:cat_id>/', products.products, name='category'),
    path('products/price/<int:product_id>/', products.get_price),
]
