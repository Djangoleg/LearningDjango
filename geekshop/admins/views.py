from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.forms import

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, ProductAdminEditForm, CategoryAdminEditForm
from geekshop.mixin import CustomDispatchMixin
from products.models import Product, ProductCategory
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-read.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(data=request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         if self.send_verify_mail(user):
    #             user_message = f"На адрес {user.email} отправлено письмо с кодом подтверждения. Пройдите по ссылке " \
    #                            f"указанной в письме, для завершения регистрации "
    #             messages.success(request, user_message)
    #         return HttpResponseRedirect(reverse('admins:admins_user_create'))
    #     return HttpResponseRedirect(reverse('admins:admins_user_create'))


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admins_user')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-read.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Продукты'
        return context


class ProductCreateView(CreateView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-products-create.html'
    form_class = ProductAdminEditForm
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание продукта'
        return context


class ProductUpdateView(UpdateView, CustomDispatchMixin):
    model = Product
    form_class = ProductAdminEditForm
    template_name = 'admins/admin-product-update-delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление продукта'
        return context


class ProductDeleteView(DeleteView, CustomDispatchMixin):
    model = Product
    template_name = 'admins/admin-product-update-delete.html'
    success_url = reverse_lazy('admins:admins_product')

    def delete(self, request, *args, **kwargs):
        # TODO: Пока не удаляю!
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-read.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context


class CategoryCreateView(CreateView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-create.html'
    form_class = CategoryAdminEditForm
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


class CategoryUpdateView(UpdateView, CustomDispatchMixin):
    model = ProductCategory
    form_class = CategoryAdminEditForm
    template_name = 'admins/admin-category-update-delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление категории'
        return context


class CategoryDeleteView(DeleteView, CustomDispatchMixin):
    model = ProductCategory
    template_name = 'admins/admin-category-update-delete.html'
    success_url = reverse_lazy('admins:admins_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    queries_list = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in queries_list]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_product_category_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
