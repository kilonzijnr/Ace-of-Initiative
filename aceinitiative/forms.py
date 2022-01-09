from django import forms
from .models import Profile,Project,Ratings
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
        fields = ['name', 'email', 'profile_pic']

class NewProjectForm(forms.ModelForm):
    """Form for uploading a new project"""
    class Meta:
        model = Project
        exclude = ['user']

class RatingsForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields =['design_vote', 'usability_vote', 'content_vote', 'comment'] 

    




