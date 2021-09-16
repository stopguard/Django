from django.db import models
from django.conf import settings
from products.models import Product


# Create your models here.
class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукты {self.product.name}'

    def sum_price(self):
        return self.count * self.product.price

    def sum_counts(self):
        items = Basket.objects.filter(user=self.user)
        quantity = 0
        for item in items:
            quantity += item.count
        return quantity

    def full_cost(self):
        items = Basket.objects.filter(user=self.user)
        cost = 0
        for item in items:
            cost += item.count * item.product.price
        return cost

