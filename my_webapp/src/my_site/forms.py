from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import MySiteProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='example@gmail.com')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateImgForm(forms.ModelForm):
    class Meta:
        model = MySiteProfile
        fields = ['image']