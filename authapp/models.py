from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)

    def user_basket_count(self):
        items = self.basket.all()
        quantity = 0
        for item in items:
            quantity += item.count
        return quantity

    def user_basket_cost(self):
        items = self.basket.all()
        cost = 0
        for item in items:
            cost += item.count * item.product.price
        return cost
