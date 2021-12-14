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

@login_required(login_url='/accounts/login/')
def search_project(request):
    """Functionality for searching for a specific project"""
    if "project" in request.GET and request.GET["project"]:
        search_term = request.GET("project")
        searched_projects = Project.search_by_name(search_term)
        message = f"{search_term}"

        return render(request,'search.html',{"message":message,"projects":searched_projects,"project":search_term})
    else:
        message = "Enter a valid project name"
        return render(request,'search.html',{"message":message})


