from django import forms
from .models import Profile,Project
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Define your forms here
class RegisterForm(UserCreationForm):
    """Form for registering a new user"""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = Profile
        exclude = ['user','email']

class NewProjectForm(forms.ModelForm):
    """Form for uploading a new project"""
    class Meta:
        model = Project
        exclude = ['user']
    




