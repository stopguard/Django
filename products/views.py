from django.shortcuts import render


# Create your views here.
# Controller-functions
def index(request):
    return render(request, 'index.html')


def products(request):
    return render(request, 'products.html')
