from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now

from geekshop import settings


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.IntegerField('Возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)

    @cached_property
    def basket_info(self):
        items = self.basket.select_related('product')
        quantity = sum(item.count for item in items)
        cost = sum(item.count * item.product.price for item in items)
        return {'qte': quantity, 'cost': cost}

    @cached_property
    def user_basket_count(self):
        items = self.basket.all()
        quantity = 0
        for item in items:
            quantity += item.count
        return quantity

    @cached_property
    def user_basket_cost(self):
        items = self.basket.select_related('product')
        cost = 0
        for item in items:
            cost += item.count * item.product.price
        return cost

    @cached_property
    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=48)

    def send_verify_mail(self):
        verify_link = reverse('auth:verify_mail', args=[self.username, self.activation_key])
        title = f'Подтверждение учётной записи {self.username}'
        message = f'Для подтверждения учётной записи {self.username} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке:\n' \
                  f'{settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
    )

    user = models.OneToOneField(get_user_model(), primary_key=True, on_delete=models.CASCADE)
    tagline = models.CharField('теги', max_length=128, blank=True)
    about_me = models.TextField('о себе', blank=True)
    gender = models.CharField('пол', max_length=1, choices=GENDER_CHOICES, blank=True)


# signals
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

