from django.db import models
from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modify_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price

    @staticmethod
    def total_sum(user):
        baskets = Basket.objects.filter(user=user)
        return sum([x.sum() for x in baskets])

    @staticmethod
    def total_quantity(user):
        baskets = Basket.objects.filter(user=user)
        return sum([x.quantity for x in baskets])
