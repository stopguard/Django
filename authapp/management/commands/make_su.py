from django.core.management.base import BaseCommand

from authapp.models import ShopUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not ShopUser.objects.filter(username='django').exists():
            ShopUser.objects.create_superuser('django', '', 'geekshop')
            print('Standard super user created')
        else:
            print('Standard user is exists')
