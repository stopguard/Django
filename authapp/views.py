from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserProfileForm, UserProfileForm
from basketapp.models import Basket


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
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(previous_page or reverse('products:index'))
    else:
        form = ShopUserLoginForm()
    context = {
        'page_title': 'GeekShop - Авторизация',
        'form': form,
        'previous_page': previous_page,
    }
    return render(request, 'authapp/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if user.send_verify_mail():
                messages.add_message(request,
                                     messages.SUCCESS,
                                     'Пользователь зарегистрирован!\n'
                                     'На указанный email отправлено письмо со ссылкой для подтверждения регистрации')
            else:
                messages.add_message(request, messages.WARNING, 'Не удалось отправить письмо на указанный email')
                user.delete()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context = {
        'page_title': 'GeekShop - Регистрация',
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', context)


@login_required
@transaction.atomic
def profile(request):
    if request.method == 'POST':
        user_form = ShopUserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileForm(data=request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Профиль отредактирован!')
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        user_form = ShopUserProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    basket = Basket.objects.filter(user=request.user)
    context = {
        'page_title': 'GeekShop - Профиль',
        'user_form': user_form,
        'profile_form': profile_form,
        'basket': basket,
        'object': request.user
    }
    return render(request, 'authapp/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:index'))


def verify_mail(request, username, activation_key):
    try:
        user = get_user_model().objects.get(username=username)  # использовал имя пользователя т.к. email не unique
        if user.activation_key == activation_key and not user.is_activation_key_expired:
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'Учётная запись подтверждена! Добро пожаловать!')
            return HttpResponseRedirect(reverse('products:products'))
        messages.add_message(request, messages.WARNING, f'Ошибка активации пользователя {user.username}!\n'
                                                        f'Неверная ссылка или ключ активации истёк.')
    except Exception as e:
        messages.add_message(request, messages.WARNING, f'error activation user: {e.args}')
    return HttpResponseRedirect(reverse('products:index'))
