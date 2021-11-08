from django.core.management import BaseCommand
from django.db import connection
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from prettytable import PrettyTable

from orders.models import OrderItem
from admins.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__updated__lte=F('order__created') + action_1__time_delta)

        action_2__condition = Q(order__updated__gt=F('order__created') + action_1__time_delta) & \
                              Q(order__updated__lte=F('order__created') + action_2__time_delta)

        action_expired__condition = Q(order__updated__gt=F('order__created') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition,
                               then=F('product__price') * F('quantity') * action_1__discount)

        action_2__price = When(action_2__condition,
                               then=F('product__price') * F('quantity') * -action_2__discount)

        action_expired__price = When(action_expired__condition,
                                     then=F('product__price') * F('quantity') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(), )).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'total_price').select_related()

        report_table = PrettyTable(['Заказ', 'Товар', 'Скидка', 'Время'])
        report_table.align = 'l'
        for orderitem in test_orders:
            report_table.add_row([f'{orderitem.action_order:2}: заказ №{orderitem.pk:3}',
                                  f'{orderitem.product.name:15}',
                                  f'{abs(orderitem.total_price):6.2f} руб.',
                                  orderitem.order.updated - orderitem.order.created])

        print(report_table)

        db_profile_by_type('Test report', 'SELECT', connection.queries)
