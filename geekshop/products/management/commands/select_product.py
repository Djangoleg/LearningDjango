from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q

from products.models import Product
from admins.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.filter(Q(category__name='Тестовая категория') | Q(category__name='Обувь'))
        print(products)
        db_profile_by_type('products sql', 'SELECT', connection.queries)
