from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class SigninForm():
    pass