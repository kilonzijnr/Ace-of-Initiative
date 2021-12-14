
  
from rest_framework import serializers
from .models import Profile,Project

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model fields"""
    class Meta:
        model=Profile
        fields=('bio','email','profile_pic','user')

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project model fields"""
    class Meta:
        model=Project
        fields=('projectimage','name','description','link','profile',)  