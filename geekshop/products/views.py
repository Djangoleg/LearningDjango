import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
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
            link_category = ProductCategory.objects.filter(is_active=True)
            cache.set(key, link_category)
        return link_category
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_link_product():
    if settings.LOW_CACHE:
        key = 'links_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.filter(is_active=True).order_by('price').select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.filter(is_active=True).order_by('price').select_related('category')


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


def get_products_in_category_orederd_by_price(category_id=None):
    if category_id:
        if settings.LOW_CACHE:
            key = f'products_in_category_orederd_by_price_{category_id}'
            products = cache.get(key)
            if products is None:
                products = Product.objects.filter(category_id=category_id, is_active=True).order_by('price')
                cache.set(key, products)
            return products
        else:
            return Product.objects.filter(category_id=category_id, is_active=True).order_by('price')
    else:
        return Product.objects.filter(is_active=True).order_by('price')


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = ProductCategory.objects.filter(pk=pk, is_active=True)
            cache.set(key, category)
        return category
    else:
        return ProductCategory.objects.filter(pk=pk, is_active=True)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    success_url = reverse_lazy('products:index')

    @staticmethod
    def get_all(request):

        request.session['category_id'] = None
        request.session['page_id'] = None
        paginator = Paginator(get_link_product(), per_page=3)
        products_paginator = paginator.page(1)

        content = {"title": "GeekShop",
                   "currency": "руб",
                   "categories": get_links_category(),
                   "products": products_paginator}

        return render(request, 'products/products.html', content)

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Каталог'
        context['currency'] = "руб"

        category_id = None
        page_id = 1

        if 'category_id' in self.kwargs:
            category_id = self.kwargs['category_id']
        elif self.request.session['category_id']:
            category_id = self.request.session['category_id']

        if category_id:
            # Передача в сессию ИД выбранный категории. Далее используется при формировании корзины в baskets\views.py
            self.request.session['category_id'] = category_id
            context['categories'] = get_category(category_id)
        else:
            context['categories'] = get_links_category()

        if 'page_id' in self.kwargs:
            page_id = self.kwargs['page_id']
            self.request.session['page_id'] = page_id
        elif self.request.session['page_id']:
            page_id = self.request.session['page_id']

        # products = Product.objects.filter( category_id=category_id).order_by('id') if category_id is not None else
        # Product.objects.all().order_by('id')

        products = get_products_in_category_orederd_by_price(
            category_id) if category_id is not None else get_link_product()

        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator

        return context

    def get_products_ajax(self, request, *args, **kwargs):
        category_id = int()

        if 'category_id' in kwargs:
            category_id = kwargs.get('category_id')
        elif request.session['category_id']:
            category_id = request.session.get('category_id')

        page_id = 1
        if 'page_id' in kwargs:
            page_id = kwargs['page_id']
            request.session['page_id'] = page_id
        elif request.session['page_id']:
            page_id = request.session['page_id']

        # if request.is_ajax():
        links_menu = get_links_menu()

        if category_id == 0:
            category = get_links_menu()
            products = get_link_product()
        else:
            # Передача в сессию ИД выбранный категории. Далее используется при формировании корзины в baskets\views.py
            request.session['category_id'] = category_id
            category = get_category(category_id)
            products = get_products_in_category_orederd_by_price(category_id)

        paginator = Paginator(products, 3)
        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'links_menu': links_menu,
            'categories': category,
            'products': products_paginator,
            'currency': "руб",
        }

        result = render_to_string(
            'include/products_list_content.html',
            context=content,
            request=request)

        return JsonResponse({'result': result})


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
        context['categories'] = get_links_category()
        return context
