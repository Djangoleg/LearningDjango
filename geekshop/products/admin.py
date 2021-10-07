from django.contrib import admin
from products.models import Product, ProductCategory

# Register your models here.
# admin.site.register(Product)
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description', 'price', 'quantity', 'category')
    # Если нужно поля на одну строчку, то объединяем в кортежи.
    fields = ('name', 'image', 'description', ('price', 'quantity'), 'category',)
    readonly_fields = ('description',)
    ordering = ('name',)
    search_fields = ('name',)


