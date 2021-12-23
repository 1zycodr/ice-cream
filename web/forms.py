from django import forms
from web import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = ('title', 'description',
                  'price', 'category', 'image')


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        print('save!')
        return super().save(commit)
