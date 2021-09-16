from django.shortcuts import render, HttpResponseRedirect, get_object_or_404

from basketapp.models import Basket
from products.models import Product


# Create your views here.
def basket_add(request, prod_id):
    basket_item, _ = Basket.objects.get_or_create(user=request.user, product_id=prod_id)
    basket_item.count += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, prod_id):
    context = {}
    return render(request, '', context)

