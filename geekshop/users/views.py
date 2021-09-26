from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

# Create your views here.
from users.forms import UserLoginForm, UserRegisterForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        # Пустая форма если запрос не POST.
        form = UserLoginForm()

    content = {
        'title': 'GeekShop - Авторизация',
        'form': form,
    }

    return render(request, 'users/login.html', content)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешная регистрация!')
            return HttpResponseRedirect(reverse('users:login'))
    else:
        # Пустая форма если запрос не POST.
        form = UserRegisterForm()

    content = {
        'title': 'GeekShop - Регистрация',
        'form': form,
    }

    return render(request, 'users/register.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))