from django.urls import path, include

from .views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView, ProductListView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryListView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

app_name = 'admins'

urlpatterns = (
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users_create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users_update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users_delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),

    path('products/', ProductListView.as_view(), name='admins_product'),
    path('products_create/', ProductCreateView.as_view(), name='admins_product_create'),
    path('products_update/<int:pk>/', ProductUpdateView.as_view(), name='admins_product_update'),
    path('products_delete/<int:pk>/', ProductDeleteView.as_view(), name='admins_product_delete'),

    path('category/', CategoryListView.as_view(), name='admins_category'),
    path('category_create/', CategoryCreateView.as_view(), name='admins_category_create'),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name='admins_category_update'),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name='admins_category_delete'),
)

