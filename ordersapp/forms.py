from django.forms import ModelForm, HiddenInput, FloatField

from ordersapp.models import Order, OrderItem


class BaseOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'user':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'


class OrderForm(BaseOrderForm):
    class Meta:
        model = Order
        fields = ('user', )


class OrderItemForm(BaseOrderForm):
    price = FloatField(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'
