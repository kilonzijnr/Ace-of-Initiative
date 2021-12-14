
  
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from . import views

#URL's here
urlpatterns=[
    url('^$',views.homepage,name='homepage'),
    url('profile',views.view_profile,name='view_profile'),
    url('^search/', views.search_project, name='search_project'),
    url('^new/project$', views.new_project, name='new_project'),
    url('^awwardsapi/api/profile/$', views.ProfileList.as_view(),name='api-profile'),
    url('^awwardsapi/api/project/$', views.ProjectList.as_view(),name='api-project'),
    url('^awwardsapi/$',views.api_page,name='api-page'),
    url('register/',views.register, name='register'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)