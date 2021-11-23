from django.urls import path

import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='index'),
    path('create/', ordersapp.OrderCreate.as_view(), name='create'),
    path('change/<int:pk>/', ordersapp.OrderUpdate.as_view(), name='change'),
    path('detail/<int:pk>/', ordersapp.OrderRead.as_view(), name='detail'),
    path('del/<int:pk>/', ordersapp.OrderDelete.as_view(), name='del'),
    path('confirm/<int:pk>/', ordersapp.order_forming_complete, name='confirm'),
]
