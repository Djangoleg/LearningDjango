import datetime
import json
from django.shortcuts import render

from .models import ProductCategory, Product


# Create your views here.

def index(request):
    content = {
        'title': 'GeekShop',
        'header': 'GeekShop Store',
        'description': f"Новые образы и лучшие бренды на GeekShop Store.\n"
                       f"Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.",
    }
    return render(request, 'products/index.html', content)


def products(request):

    my_products = Product.objects.all()[:4]
    content = {"title": "GeekShop",
               "currency": "руб",
               "date": datetime.datetime.now(),
               "products": my_products}

    return render(request, 'products/products.html', content)
