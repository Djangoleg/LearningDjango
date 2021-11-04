from django.urls import path
from django.views.decorators.cache import never_cache

from .views import LoginListView, RegisterListView, Logout, ProfileFormView

app_name = 'users'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', never_cache(RegisterListView.as_view()), name='register'),
    path('profile/', never_cache(ProfileFormView.as_view()), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),

    path('verify/<str:email>/<str:activation_key>/', RegisterListView.verify, name='verify'),
]
