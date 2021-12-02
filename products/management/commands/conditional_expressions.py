from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q, F, When, Case, IntegerField, DecimalField

from ordersapp.models import OrderItem
from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_td = timedelta(hours=12)
        action_2_td = timedelta(days=1)

        action_1_disc = 0.3
        action_2_disc = 0.15
        action_exp_disc = 0.05

        action_1_cond = Q(order__update_datetime__lte=F('order__add_datetime') + action_1_td)

        action_2_cond = Q(order__update_datetime__gt=F('order__add_datetime') + action_1_td) & \
                        Q(order__update_datetime__lte=F('order__add_datetime') + action_2_td)

        action_exp_cond = Q(order__update_datetime__gt=F('order__add_datetime') + action_2_td)

        action_1_ord = When(action_1_cond, then=ACTION_1)
        action_2_ord = When(action_2_cond, then=ACTION_2)
        action_exp_ord = When(action_exp_cond, then=ACTION_3)

        action_1_delta_cost = When(action_1_cond, then=F('product__price') * F('count') * action_1_disc)
        action_2_delta_cost = When(action_2_cond, then=F('product__price') * F('count') * -action_2_disc)
        action_exp_delta_cost = When(action_exp_cond, then=F('product__price') * F('count') * action_exp_disc)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1_ord,
                action_2_ord,
                action_exp_ord,
                output_field=IntegerField(),
            )
        ).annotate(
            delta_cost=Case(
                action_1_delta_cost,
                action_2_delta_cost,
                action_exp_delta_cost,
                output_field=DecimalField(),
            )
        ).order_by('action_order', 'delta_cost').select_related('order', 'product')

        for order_item in test_orders:
            print(f'{order_item.action_order:2} | '
                  f'заказ №{order_item.order.pk:3} | '
                  f'предмет №{order_item.pk:3} | '
                  f'{order_item.product.name:70} | '
                  f'цена {order_item.sum_price:15.2f} руб. | '
                  f'скидка {abs(order_item.delta_cost):15.2f} руб. | '
                  f'{str(order_item.order.update_datetime - order_item.order.add_datetime):>25}')

        print(Product.objects.filter(Q(id__lte=5) | ~Q(is_active=False)).select_related('category'))
