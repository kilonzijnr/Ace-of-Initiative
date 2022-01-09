from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max

# Create your models here.
class Profile(models.Model):
    """Class model for user profile"""
    profile_pic = models.ImageField(upload_to='profilepic/')
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=70, blank=True)
    email= models.EmailField()
    bio = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def save_profile(self):
        self.save()

class Project(models.Model):
    """Class model for the project fields"""
    projectimage = models.ImageField(upload_to='projectimage', null=True)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.CharField(max_length=150)
    

    def __str__(self):
        return self.name

    def save_project(self):
        self.save()
        
    @classmethod
    def search_by_name(cls, search_term):
        """Class method to source a project"""
        projects = cls.objects.filter(name_icontains = search_term)
        return projects

class Rating(models.Model):
    rating=(
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )


    design = models.IntegerField(choices=rating, default=0, blank=True)
    usability = models.IntegerField(choices=rating, blank=True)
    content = models.IntegerField(choices=rating, blank=True)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(project_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.project} Rating'

    """Class model for Project Ratings"""

