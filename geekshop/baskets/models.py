from django.db import models
from users.models import User
from products.models import Product


# class BasketQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(BasketQuerySet, self).delete()


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modify_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def sum(self):
        return self.quantity * self.product.price

    # def delete(self, using=None, keep_parents=False):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete()
    #
    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.get_items(pk=self.pk)
    #     else:
    #         self.product.quantity -= self.quantity
    #
    #     self.product.save()
    #
    #     super(Basket, self).save()

    @staticmethod
    def total_sum(user):
        baskets = Basket.objects.filter(user=user)
        return sum([x.sum() for x in baskets])

    @staticmethod
    def total_quantity(user):
        baskets = Basket.objects.filter(user=user)
        return sum([x.quantity for x in baskets])

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first().quantity
