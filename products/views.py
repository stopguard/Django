from django.shortcuts import render
from datetime import datetime
from json import load


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
        'products': extract_data('db.json')
    }
    return render(request, 'products.html', context)


def extract_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = load(f)
    return data
