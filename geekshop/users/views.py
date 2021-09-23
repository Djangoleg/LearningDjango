from django.shortcuts import render


# Create your views here.
def login(request):
    content = {
        'title': 'GeekShop - Авторизация'
    }
    return render(request, 'users/login.html', content)


def register(request):
    content = {
        'title': 'GeekShop - Регистрация'
    }
    return render(request, 'users/register.html', content)
