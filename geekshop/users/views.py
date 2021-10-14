from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

# Create your views here.
from users.models import User
from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = 'Geekshop - Регистрация'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                user_message = f"На адрес {user.email} отправлено письмо с кодом подтверждения. Пройдите по ссылке " \
                               f"указанной в письме, для завершения регистрации "
                messages.success(request, user_message)
            return redirect(self.success_url)
        return redirect(self.success_url)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Geekshop - Профайл'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return redirect(self.success_url)


class Logout(LogoutView):
    template_name = 'products/index.html'


def send_verify_mail(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ' \
              f'ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user=user)
        return render(request, 'users/verification.html')
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('index'))
