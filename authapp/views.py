from datetime import datetime

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('products:index'))
    else:
        form = ShopUserLoginForm()
    context = {
        'page_title': 'GeekShop - Авторизация',
        'form': form,
        'div_class': 'col-lg-5',
        'label': 'Авторизация',
    }
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'page_title': 'GeekShop - Регистрация',
        'div_class': 'col-lg-7',
        'label': 'Создать аккаунт',
        'today': datetime.now(),
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))

