"""fitnesstrainer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from mysite.core import views as core_views
from django.urls import path
from django.contrib.auth import views as auth_views
from AIfitnesstrainer import  views

urlpatterns = [
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.signup, name='signup'),
    url(r'^goal/delete/(?P<value>\d+)/$', views.goaldelete, name='goaldelete'),
    url(r'^goal/update/(?P<value>\d+)/$',views.goalupdateform,name='goalupdatelist'),
    url(r'^mealtype/delete/(?P<value>\d+)/$', views.mealtypedelete, name='mealtypedelete'),
    url(r'^mealtype/update/(?P<value>\d+)/$',views.mealsupdateform,name='mealsupdatelist'),
    url(r'^meals/delete/(?P<value>\d+)/$', views.mealsdelete, name='mealsdelete'),
    url(r'^meals/update/(?P<value>\d+)/$',views.mealsupdateform,name='mealsupdatelist'),
    url(r'^supplements/delete/(?P<value>\d+)/$', views.supplementsdelete, name='supplementsdelete'),
    url(r'^supplements/update/(?P<value>\d+)/$', views.supplementsupdateform, name='supplementsupdatelist'),
    url(r'^home_workout/delete/(?P<value>\d+)/$', views.home_workoutdelete, name='home_workoutdelete'),
    url(r'^home_workout/update/(?P<value>\d+)/$', views.home_workoutupdateform, name='home_workoutupdatelist'),


    path('',views.index,name='index'),
    path('admin/', admin.site.urls),
    path('home',views.home,name='home'),

    path('goal',views.goalform,name='goal'),
    path('goal/list',views.goallist,name='goallist'),
    path('goal/update',views.goalupdate,name='goalupdate'),

    path('mealtype', views.mealtypeform, name='mealtype'),
    path('mealtype/list', views.mealtypelist, name='mealtypelist'),
    path('mealtype/update', views.mealtypeupdate, name='mealtypeupdate'),

    path('meals', views.mealsform, name='meals'),
    path('meals/list', views.mealslist, name='mealslist'),
    path('meals/update', views.mealsupdate, name='mealsupdate'),

    path('supplements', views.supplementsform, name='supplements'),
    path('supplements/list', views.supplementslist, name='supplementslist'),
    path('supplements/update', views.supplementsupdate, name='supplementsupdate'),

    path('home_workout', views.home_workoutform, name='home_workout'),
    path('home_workout/list', views.home_workoutlist, name='home_workoutlist'),
    path('home_workout/update', views.home_workoutupdate, name='home_workoutupdate'),


]
