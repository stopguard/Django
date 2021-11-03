from django.contrib.auth.forms import UserChangeForm
from django import forms as forms_lib
from django.forms import forms

from authapp.forms import ShopUserProfileForm
from products.models import ProductsCategory, Product


class ShopUserEditForm(ShopUserProfileForm):
    email = forms_lib.EmailField(widget=forms_lib.EmailInput(
        attrs={'class': 'form-control py-4', 'readonly': False}))
    username = forms_lib.CharField(widget=forms_lib.TextInput(
        attrs={'class': 'form-control py-4', 'readonly': False}))


class CategoryForm(forms_lib.ModelForm):
    name = forms_lib.CharField(widget=forms_lib.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Название'}))
    description = forms_lib.CharField(widget=forms_lib.TextInput(
        attrs={'class': 'form-control py-4', 'placeholder': 'Описание'}))

    class Meta:
        model = ProductsCategory
        fields = ('name', 'description')


class ProductForm(forms_lib.ModelForm):
    category = forms_lib.ModelChoiceField(
        widget=forms_lib.Select(attrs={'class': 'form-control',
                                       'placeholder': 'Категория'}),
        queryset=ProductsCategory.objects.filter(is_active=True))
    name = forms_lib.CharField(widget=forms_lib.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Название'}))
    image = forms_lib.ImageField(widget=forms_lib.FileInput(
        attrs={'class': 'custom-file-input'}), required=False)
    description = forms_lib.CharField(widget=forms_lib.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Описание', 'style': 'height: 100px'}), required=False)
    price = forms_lib.DecimalField(widget=forms_lib.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Цена'}))
    quantity = forms_lib.IntegerField(widget=forms_lib.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Количество'}))

    class Meta:
        model = Product
        fields = ('category', 'name', 'image', 'description', 'price', 'quantity')
