from django.urls import path, include

from .views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'admins'

urlpatterns = (
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_user'),
    path('users_create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users_update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users_delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),
)
