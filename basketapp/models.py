from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукты {self.product.name}'

    @cached_property
    def sum_price(self):
        return self.count * self.product.price
