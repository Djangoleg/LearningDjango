from django.shortcuts import render

# Create your views here.
from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from orders.models import Order, OrderItem


class OrderList(ListView):
    pass


class OrderCreate(CreateView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DeleteView):
    pass


class OrderDetail(DetailView):
    pass


def order_forming_complete(request, pk):
    pass
