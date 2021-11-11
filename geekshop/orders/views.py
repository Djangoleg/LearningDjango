from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django import forms
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin
from orders.forms import OrderItemsForm
from orders.models import Order, OrderItem
from products.models import Product


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    # template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Создать заказ'

        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderItemFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=basket_item.count())
                formset = OrderItemFormSet()

                for ind, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[ind].product
                    form.initial['quantity'] = basket_item[ind].quantity
                    form.initial['price'] = basket_item[ind].product.price
                basket_item.delete()
            else:
                formset = OrderItemFormSet()

        context['orderitems'] = formset

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_items = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Обновление заказа'

        OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=1)

        if self.request.POST:
            # order_items_count = OrderItem.objects.filter(order_id=self.object.pk).count()
            # OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemsForm, extra=order_items_count)
            formset = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderItemFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView, BaseClassContextMixin):
    model = Order
    title = 'GeekShop | Просмотр заказа'

    @staticmethod
    def get_product_price(request, product_id):
        price = float()
        if request.is_ajax():
            try:
                price = Product.objects.filter(id=product_id).first().price
            except AttributeError as e:
                print(e)

        return JsonResponse({'price': price})


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('orders:list'))


def status_change(request, pk):
    order = get_object_or_404(Order, pk=pk)
    index = Order.statuses.index(order.status)
    if index == len(Order.statuses) - 1:
        index = 0
    else:
        index += 1
    order.status = Order.statuses[index]
    order.save()

    return HttpResponseRedirect(reverse('orders:list'))
