from django.shortcuts import render,edirect
from .models import Profile,Project



# Create your views here.
def homepage(request):
    """Default landing page"""
    projects = Project.objects.all()
    return render(request,'home.html',{'projects':projects})
    
