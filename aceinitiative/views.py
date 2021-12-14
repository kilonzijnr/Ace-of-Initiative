from django.shortcuts import redirect, render,edirect
from .models import Profile,Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NewProjectForm,RegistrationForm,ProfileUpdateForm
from django.contrib.auth.models import User




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

def userregistration(request):
    """Functionality for registering a new user"""
    if request.method == 'POST':
        username=request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user = User.objects.create_user(username=username,email=email,password=password1) 
        user.save()
        profile = Profile.objects.create(user=user,email=email)

        return redirect('login')
    else:
        return render(request,'registration/signup.html')




