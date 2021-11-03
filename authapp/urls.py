from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('profile/', authapp.profile, name='profile'),
    path('verify/<str:username>/<str:activation_key>/', authapp.verify_mail, name='verify_mail'),
]
