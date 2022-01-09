from django.http import response
from django.shortcuts import redirect, render
from rest_framework import serializers
from .models import Profile,Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NewProjectForm,RegisterForm,ProfileUpdateForm
from django.contrib.auth.models import User

from rest_framework.response import Response
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.views import APIView


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

def register(request):
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

@login_required(login_url='/accounts/login/')
def new_project(request):
    """Functionality for uploading a new project"""
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('homepage')
    else:
        form = NewProjectForm()
    return render(request,'project.html',{"form":form,"current_user":current_user})

@login_required(login_url='/accounts/login/')
def api_page(request):
    return render(request,'apiends.html')

class ProfileList(APIView):
    """API class for returning Profile fields in API view"""
    def get(self,request,fromat=None):
        all_profiles= Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    """API class for returning Project fields in API view"""
    def get(self, request, fromat=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
