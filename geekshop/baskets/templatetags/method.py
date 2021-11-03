from django import template
from ..models import Basket

register = template.Library()


@register.filter(name='total_quantity')
def total_quantity(value, user):
    basket = Basket()
    basket.user = user
    return basket.total_quantity()


@register.filter(name='total_sum')
def total_sum(value, user):
    basket = Basket()
    basket.user = user
    return basket.total_sum()
