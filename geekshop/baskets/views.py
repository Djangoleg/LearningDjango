from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import redirect

from django.template.loader import render_to_string
from django.urls import reverse_lazy

from django.views.generic import DeleteView, CreateView, UpdateView

from baskets.models import Basket
from geekshop.mixin import UserDispatchMixin
from products.models import Product, ProductCategory
from products.views import get_products_in_category_orederd_by_price


class BasketCreateView(CreateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'products/products.html'
    success_url = reverse_lazy('products:index')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'product_id' in kwargs:
            product_id = kwargs['product_id']
            if product_id:
                product = Product.objects.get(id=product_id)
                baskets = Basket.objects.filter(user=request.user, product=product)
                if not baskets.exists():
                    Basket.objects.create(user=request.user, product=product, quantity=1)
                else:
                    basket = baskets.first()
                    # basket.quantity += 1
                    basket.quantity = F('quantity') + 1
                    basket.save()

        category_id = self.request.session['category_id']

        products = get_products_in_category_orederd_by_price(category_id)

        page_id = 1
        if request.POST.get('page_id'):
            page_id = int(request.POST.get('page_id'))

        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page_id)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'products': products_paginator,
            'currency': "руб",
        }

        # self.request.session['category_id'] = None

        result = render_to_string('include/product_items.html', context, request=request)

        return JsonResponse({'result': result})


class BasketDeleteView(DeleteView, UserDispatchMixin):
    model = Basket
    success_url = reverse_lazy('users:profile')


class BasketUpdateView(UpdateView, UserDispatchMixin):
    model = Basket
    fields = ['product']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    pk_url_kwarg = 'basket_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        super(BasketUpdateView, self).get(request, *args, **kwargs)
        if request.is_ajax():
            basket_id = kwargs[self.pk_url_kwarg]
            quantity = kwargs['quantity']
            basket = Basket.objects.filter(id=basket_id).order_by('created_on')
            if basket.exists():
                basket = basket.first()
                if quantity > 0:
                    basket.quantity = quantity
                    basket.save()
                else:
                    basket.delete()

            result = render_to_string('baskets/baskets.html', request=request)

            return JsonResponse({'result': result})

        return redirect(self.success_url)
