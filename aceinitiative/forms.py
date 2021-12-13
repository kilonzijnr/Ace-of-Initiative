from django import forms
from django.forms import fields
from .models import Profile,Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Define your forms here
class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        