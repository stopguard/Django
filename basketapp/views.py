from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect

from basketapp.models import Basket


# Create your views here.
@login_required
def basket_add(request, prod_id):
    basket_item, _ = Basket.objects.get_or_create(user=request.user, product_id=prod_id)
    basket_item.count += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
        basket_count = request.user.user_basket_count()
        basket_cost = request.user.user_basket_cost()
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
