from django.contrib import admin

from authapp.models import ShopUser, UserProfile

admin.site.register(ShopUser)
admin.site.register(UserProfile)
