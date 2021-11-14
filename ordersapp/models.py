from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


class Order(models.Model):
    FORMING = 'C'
    SENT = 'S'
    APPROVED = 'A'
    REJECTED = 'R'

    STATUS_CHOICES = (
        (FORMING, 'создан'),
        (SENT, 'оплачен'),
        (APPROVED, 'подтверждён'),
        (REJECTED, 'отменён'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    status = models.CharField('статус', max_length=1,
                              choices=STATUS_CHOICES,
                              default=FORMING)
    add_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('активен', default=True)

    def __str__(self):
        return f'Заказ для {self.user.username} | №{self.pk:0>8}'

    @property
    def is_forming(self):
        return self.status == self.FORMING

    @property
    def items_count(self):
        return sum(map(lambda x: x.count, self.items.all()))

    @property
    def items_cost(self):
        return sum(map(lambda x: x.sum_price, self.items.all()))

    def delete(self, using=None, keep_parents=False, safe=True):
        if safe:
            self.is_active = False
            self.status = self.REJECTED
            self.save()
            return
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        ordering = ('-add_datetime', )
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='количество', default=0)

    @property
    def sum_price(self):
        return self.count * self.product.price
