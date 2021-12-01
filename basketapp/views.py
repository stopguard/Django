from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from geekshop.settings import LOGIN_URL
from products.models import Product


# Create your views here.
@login_required
def basket_add(request, prod_id, user_id):
    if LOGIN_URL in request.META.get('HTTP_REFERER'):
        product = Product.objects.filter(id=prod_id).first()
        cat_id = 0
        if product:
            cat_id = product.category_id
        return HttpResponseRedirect(reverse('products:category', kwargs={'cat_id': cat_id}))
    if request.is_ajax():
        user = get_user_model().objects.filter(id=user_id).first()
        user = user if user else request.user
        if not Product.objects.filter(id=prod_id, quantity__gt=0):
            return JsonResponse({'status': False})  # сделать когда-нибудь оповещалку об отсутствии на складе
        basket_item, _ = Basket.objects.get_or_create(user=user, product_id=prod_id)
        basket_item.count += 1
        basket_item.save()
        if user_id != 0:
            user_basket = user.basket.select_related('product')
            user_basket_count = user.user_basket_count
            context = {
                'object': user,
                'basket': user_basket,
            }
            basket_html = render_to_string('basket/basket.html', request=request, context=context)
            return JsonResponse({'status': True, 'basket': basket_html, 'basket_count': user_basket_count, })
        return JsonResponse({'status': True})


@login_required
def basket_edit(request, item_id, val):
    if request.is_ajax():
        item = Basket.objects.filter(id=item_id).first()
        if not item:
            return JsonResponse({'status': False})
        product_count = item.product.quantity
        item_cost = 0
        if val:
            val = val if val <= product_count else product_count
            item.count = val
            item.save()
            item_cost = item.sum_price()
        else:
            item.delete()
        basket_info = item.user.basket_info
        basket_count = basket_info['qte']
        basket_cost = basket_info['cost']
        data = {
            'status': True,
            'item_cost': item_cost,
            'item_count': val,
            'basket_cost': basket_cost,
            'basket_count': basket_count,
        }
        return JsonResponse(data)


@login_required
def basket_remove(request, id):
    Basket.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
