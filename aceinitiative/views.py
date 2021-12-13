from django.shortcuts import render,edirect
from .models import Profile,Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NewProjectForm,RegistrationForm,ProfileUpdateForm




# Create your views here.
def homepage(request):
    """Default landing page"""
    projects = Project.objects.all()
    return render(request,'home.html',{'projects':projects})

@login_required(login_url='/accounts/login/')
def view_profile(request):
    """Functionality for viewing user profile"""
    projects=request.user.profile.project_set.all()
    profile=request.user.profile
    form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        context={'form':form,'projects':projects}
    return render(request,"profile.html",context=context)
    


