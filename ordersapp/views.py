from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserVerifyMixin:
    def user_verify_function(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Order, pk=pk)
        return self.request.user.is_superuser or self.request.user == obj.user

    def get(self, request, *args, **kwargs):
        if not self.user_verify_function():
            messages.warning(request, 'Это заказ другого пользователя!')
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)


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


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    extra_context = {'page_title': 'Список заказов', }

    def get_queryset(self):
        return self.request.user.orders.all()


class OrderCreate(LoginRequiredMixin, OrderFormsMixin, CreateView):
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


class OrderUpdate(UserVerifyMixin, OrderFormsMixin, UpdateView):
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


class OrderDelete(UserVerifyMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')
    extra_context = {'page_title': f'Удаление заказа', }


class OrderRead(UserVerifyMixin, DetailView):
    model = Order
    extra_context = {'page_title': f'Детали заказа', }


@login_required
def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user == order.user:
        try:
            with transaction.atomic():
                order.send_products()
                order.status = order.SENT
                order.save()
        except ValidationError as err:
            messages.warning(request, f'Ошибка! {err.message}')
        return HttpResponseRedirect(reverse('orders:index'))
    else:
        messages.warning(request, f'Ошибка! Это не ваш заказ!')
        return HttpResponseRedirect(reverse('orders:index'))
