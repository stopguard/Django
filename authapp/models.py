from datetime import timedelta

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.urls import reverse
from django.utils.timezone import now

from geekshop import settings


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.IntegerField('Возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)

    def user_basket_count(self):
        items = self.basket.all()
        quantity = 0
        for item in items:
            quantity += item.count
        return quantity

    def user_basket_cost(self):
        items = self.basket.all()
        cost = 0
        for item in items:
            cost += item.count * item.product.price
        return cost

    @property
    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=48)

    def send_verify_mail(self):
        verify_link = reverse('auth:verify_mail', args=[self.username, self.activation_key])
        title = f'Подтверждение учётной записи {self.username}'
        message = f'Для подтверждения учётной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке:\n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)
