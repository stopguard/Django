from django.core.management.base import BaseCommand

from authapp.models import ShopUser, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.filter(userprofile__isnull=True)
        for user in users:
            UserProfile.objects.create(user=user)
