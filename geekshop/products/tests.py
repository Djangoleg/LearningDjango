from django.test import TestCase
from django.test.client import Client
from products.models import Product, ProductCategory
from django.core.management import call_command


class TestProductsSmoke(TestCase):
    status_code_success = 200

    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_product(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

        for product in Product.objects.all():
            response = self.client.get(f'/products/detail/{product.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_profile(self):
        response = self.client.get(f'/users/profile/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'orders', 'baskets')
