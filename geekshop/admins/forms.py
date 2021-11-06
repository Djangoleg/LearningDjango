from django import forms

from products.models import Product, ProductCategory
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class ProductAdminEditForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'quantity', 'category', 'is_active')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image' or field_name == 'category':
                field.widget.attrs['class'] = 'form-control'
            elif field_name == 'is_active':
                field.widget.attrs['style'] = 'margin-top: 20px;'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class CategoryAdminEditForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_active':
                field.widget.attrs['class'] = 'form-control py-4'
