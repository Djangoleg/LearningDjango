from django.urls import path

from .views import OrderCreate, OrderUpdate, OrderDelete, OrderDetail, OrderList, order_forming_complete, status_change, \
    get_product_price

app_name = 'orders'

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>/', OrderDetail.as_view(), name='read'),

    path('update/<int:pk>/', OrderUpdate.as_view(), name='update'),
    path('status_change/<int:pk>/', status_change, name='status_change'),

    path('delete/<int:pk>/', OrderDelete.as_view(), name='delete'),
    path('forming_complete/<int:pk>/', order_forming_complete, name='forming_complete'),

    path('get_product_price/<int:product_id>/', get_product_price, name='get_product_price'),
]