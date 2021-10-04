from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from baskets.models import Basket
from products.models import Product


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_id):
    baskets = Basket.objects.filter(id=basket_id)
    if baskets.exists():
        baskets.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        baskets = Basket.objects.filter(id=basket_id)
        if baskets.exists():
            basket = baskets.first()
            if quantity > 0:
                basket.quantity = quantity
                basket.save()
            else:
                basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets,
        }
        result = render_to_string('baskets/baskets.html', context)

        return JsonResponse({'result': result})