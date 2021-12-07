from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property

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
    add_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    update_datetime = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('активен', default=True, db_index=True)

    def __str__(self):
        return f'Заказ для {self.user} | №{self.pk:0>8}'

    @cached_property
    def is_forming(self):
        return self.status == self.FORMING

    @cached_property
    def summary(self):
        items = self.items.select_related('product')
        items_count = sum(map(lambda x: x.count, items))
        items_cost = sum(map(lambda x: x.sum_price, items))
        return {'count': items_count, 'cost': items_cost, }

    def send_products(self):
        items = self.items.select_related('product')
        for order_item in items:
            product = order_item.product
            product_qty = product.quantity
            order_item_qty = order_item.count
            if product_qty < order_item_qty:
                raise ValidationError(f'Недостаток продукта {product.name} на складе'
                                      f' (Имеется {product_qty} из {order_item_qty})')
            product.quantity -= order_item_qty
            product.save()

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
    product = models.ForeignKey(Product,
                                limit_choices_to={'is_active': True, 'category__is_active': True},
                                on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='количество', default=0)

    @cached_property
    def sum_price(self):
        return self.count * self.product.price
