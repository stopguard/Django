import hashlib
from random import random

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import forms
from django import forms as forms_lib


class ShopUserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control py-4'
            field.widget.attrs['placeholder'] = field_name.title()


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'avatar', 'age')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def clean_username(self):
        u_name = self.cleaned_data['username']
        if len(u_name) < 6:
            raise forms.ValidationError('Длина имени пользователя должна быть не меньше 6 символов')
        return u_name

    def clean_age(self):
        u_age = self.cleaned_data['age']
        if u_age < 18:
            raise forms.ValidationError('Вы слишком молоды')
        return u_age

    def save(self):
        user = super(ShopUserRegisterForm, self).save(commit=False)
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user


class ShopUserProfileForm(UserChangeForm):
    first_name = forms_lib.CharField(widget=forms_lib.TextInput(attrs={'class': 'form-control py-4',
                                                                       'placeholder': 'Введите имя'}), required=False)
    last_name = forms_lib.CharField(widget=forms_lib.TextInput(attrs={'class': 'form-control py-4',
                                                                      'placeholder': 'Введите фамилию'}),
                                    required=False)
    email = forms_lib.EmailField(widget=forms_lib.EmailInput(attrs={'class': 'form-control py-4',
                                                                    'readonly': True}))
    username = forms_lib.CharField(widget=forms_lib.TextInput(attrs={'class': 'form-control py-4',
                                                                     'readonly': True}))
    avatar = forms_lib.ImageField(widget=forms_lib.FileInput(attrs={'class': 'form-control py-4'}), required=False)
    age = forms_lib.IntegerField(widget=forms_lib.NumberInput(attrs={'class': 'form-control py-4'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'avatar', 'age', 'password')
