from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderFormsMixin:
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            order = super().form_valid(form)
            if orderitems.is_valid():
                if self.request.path == '/orders/create/':
                    orderitems.instance = self.object
                    self.request.user.basket.all().delete()
                inf = orderitems.save()

        if self.object.items_cost == 0:
            self.object.delete()
        return order


class OrderList(ListView):
    model = Order
    extra_context = {'page_title': 'Список заказов', }

    def get_queryset(self):
        return self.request.user.orders.all()


class OrderCreate(OrderFormsMixin, CreateView):
    extra_context = {'page_title': 'Новый заказ', }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'].initial['user'] = self.request.user
            basket_items = self.request.user.basket.all()
            if basket_items:
                OrderFormSet = inlineformset_factory(Order, OrderItem,
                                                     form=OrderItemForm,
                                                     extra=basket_items.count() + 1)
                formset = OrderFormSet()
                for form, item in zip(formset.forms, basket_items):
                    form.initial['price'] = item.product.price
                    form.initial['product'] = item.product
                    form.initial['count'] = item.count
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context


class OrderUpdate(OrderFormsMixin, UpdateView):
    extra_context = {'page_title': f'Редактирование заказа', }

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST,
                                   self.request.FILES,
                                   instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context['orderitems'] = formset
        return context


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')
    extra_context = {'page_title': f'Удаление заказа', }


class OrderRead(DetailView):
    model = Order
    extra_context = {'page_title': f'Детали заказа', }


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    try:
        with transaction.atomic():
            order.send_products()
            order.status = order.SENT
            order.save()
    except ValidationError as err:
        messages.warning(request, f'Ошибка! {err.message}')
    return HttpResponseRedirect(reverse('orders:index'))
