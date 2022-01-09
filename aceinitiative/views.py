from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile,Project,Ratings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import NewProjectForm,RegisterForm,ProfileUpdateForm,RatingsForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404

from rest_framework.response import Response
from .serializer import ProfileSerializer,ProjectSerializer
from rest_framework.views import APIView


# Create your views here.
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doesnt exist')

        user = authenticate(request, username= username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'username or password does not exist')

    context = {
        'page':page
    }
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('homepage')


def registerUser(request):
    page = 'register'
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'An error occured during registration')
    context = {
        'form':form,
        'page':page
    }

    return render(request, 'registration/login.html', context)



def homepage(request):
    """Default landing page"""
    projects = Project.objects.all()
    return render(request,'home.html',{'projects':projects})

@login_required(login_url='login')
def rate_project(request, id):
    current_user = request.user
    try:
        project = Project.objects.get(id = id)
    except ObjectDoesNotExist:
        raise Http404()
    ratings = project.ratings_set.all()

    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.rater = current_user
            rating.project = project
            rating.save()
            return redirect('homepage')
    else:
        form = RatingsForm()   
    
    return render(request, 'rate_project.html', {'project':project, 'form':form , 'ratings':ratings})

@login_required(login_url='login')
def view_profile(request,pk):
    """Display function for user profile"""
    current_user = request.user
    projects = Project.objects.filter(profile_id=current_user.id)
    profile = Profile.objects.filter(name=current_user).first()
    return render(request,'profile.html', {"projects":projects, "profile":profile})


@login_required(login_url='login')
def search_project(request):
    """Functionality for searching for a specific project"""
    if "search" in request.GET and request.GET["search"]:
        search_term = request.GET.get("search").lower
        projects = Project.search_by_name(search_term)
        message = f"{search_term}"
        title = message

        return render(request,'search.html',{"success":message,"projects":projects,"title":title})
    else:
        message = "Enter a valid project name"
        return render(request,'search.html',{'danger':message})

@login_required(login_url='login')
def new_project(request):
    current_user = request.user
    if request.method == "POST":
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.rater = current_user
            project.save()
        return redirect('homepage')
    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {'form':form})

def update_profile(request):
    user = request.user
    form = ProfileUpdateForm(instance=user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile', pk=user.id)
    context = {
        'form':form
    }
    return render(request, 'update_profile.html', context)

@login_required(login_url='login')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'project.html', {'projects':projects})

@login_required(login_url='login')
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
