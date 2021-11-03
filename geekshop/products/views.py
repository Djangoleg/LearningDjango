import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.core.cache import cache

from geekshop.mixin import UserDispatchMixin
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


def get_links_category():
    if settings.LOW_CACHE:
        key = 'links_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.all()


def get_link_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.all().select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['currency'] = "руб"
        context['categories'] = get_links_category()

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']

        # Передача в сессию ИД выбранный категории. Далее используется при формировании корзины в baskets\views.py
        self.request.session['category_id'] = category_id

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']

        products = Product.objects.filter(
            category_id=category_id).order_by('id') if category_id is not None else Product.objects.all().order_by('id')

        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        """Добавляем список категорий для вывода сайдбара с категориями на странице каталога"""
        context = super().get_context_data()

        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.all()
        return context
