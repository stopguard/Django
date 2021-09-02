from django.shortcuts import render
from datetime import datetime


# Create your views here.
# Controller-functions
def index(request):
    context = {
        'page_title': 'geekshop',
        'today': datetime.now(),
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'page_title': 'geekshop - каталог',
        'today': datetime.now(),
    }
    return render(request, 'products.html', context)
