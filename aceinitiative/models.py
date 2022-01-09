from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Ratings(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    design_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    usability_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    content_vote = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)



    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()
        
    def __str__(self):
        return self.rater.username

    @property
    def average_score(self):
        average = (self.design_vote + self.content_vote + self.usability_vote) /3
        return round(average, 1)


