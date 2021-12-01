from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('add/<int:prod_id>/<int:user_id>/', basketapp.basket_add, name='add'),     # AJAX
    path('remove/<int:id>/', basketapp.basket_remove, name='remove'),
    path('edit/<int:item_id>/<int:val>/', basketapp.basket_edit),       # AJAX
]
