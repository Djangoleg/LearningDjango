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

    content = {"title": "GeekShop",
               "currency": "руб",
               "categories": ProductCategory.objects.all(),
               "products": Product.objects.all()}

    return render(request, 'products/products.html', content)

