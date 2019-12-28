from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from AIfitnesstrainer.forms import SignUpForm
from AIfitnesstrainer.models import Goal
from AIfitnesstrainer.models import MealType
from AIfitnesstrainer.models import Meals
from AIfitnesstrainer.models import Supplements

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request,'index.html')
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})