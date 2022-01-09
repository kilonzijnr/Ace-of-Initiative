
  
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . views import *
from .import views

#URL's here
urlpatterns=[
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('',views.homepage,name='homepage'),
    path('view_profile/<int:pk>', views.view_profile, name='view_profile'),
    path('project/(\d+)',views.rate_project,name='rate-project'),
    path('profile',views.view_profile,name='view_profile'),
    path('search/', views.search_project, name='search_project'),
    path('new/project/', views.new_project, name='new_project'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('rate_project/<id>/', views.rate_project, name='rate_project'),
    path('api/profile/', views.ProfileList.as_view(),name='api-profile'),
    path('api/project/', views.ProjectList.as_view(),name='api-project'),
    path('awwardsapi',views.api_page,name='api_page'),
    
 
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)