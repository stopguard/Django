from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserProfileForm
from basketapp.models import Basket


# Create your views here.
def login(request):
    previous_page = request.GET.get('next', '')
    if request.method == 'POST':
        form = ShopUserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            previous_page = request.POST.get('previous_page')
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(previous_page or reverse('products:index'))
    else:
        form = ShopUserLoginForm()
    context = {
        'page_title': 'GeekShop - Авторизация',
        'today': datetime.now(),
        'form': form,
        'previous_page': previous_page,
    }
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Пользователь зарегистрирован!')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'page_title': 'GeekShop - Регистрация',
        'today': datetime.now(),
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ShopUserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Профиль отредактирован!')
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        profile_form = ShopUserProfileForm(instance=request.user)
    basket = Basket.objects.filter(user=request.user)
    context = {
        'page_title': 'GeekShop - Профиль',
        'today': datetime.now(),
        'profile_form': profile_form,
        'basket': basket,
        'object': request.user
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))
