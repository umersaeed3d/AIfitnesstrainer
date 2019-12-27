from django.shortcuts import render,redirect
from AIfitnesstrainer.models import Goal
from AIfitnesstrainer.models import MealType
from AIfitnesstrainer.models import Meals
from AIfitnesstrainer.models import Supplements

def home(request):
    return render(request, 'home.html')

# Create your views here.
