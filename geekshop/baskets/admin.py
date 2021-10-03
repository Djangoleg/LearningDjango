from django.contrib import admin

# Register your models here.
from baskets.models import Basket


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_on', 'modify_on')
    readonly_fields = ('created_on', 'modify_on')
    extra = 0
