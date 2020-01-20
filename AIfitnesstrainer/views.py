from django.shortcuts import render,redirect
from django.contrib import messages
from pprint import  pprint
from django.contrib.auth import login, authenticate
from AIfitnesstrainer.forms import SignUpForm,GoalForm,MealTypeForm
from AIfitnesstrainer.models import Goal
from AIfitnesstrainer.models import MealType
from AIfitnesstrainer.models import Meals
from AIfitnesstrainer.models import Supplements,Homeworkout
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def index(request):
    goal = Goal.objects.all()
    mealtype = MealType.objects.all()
    return render(request,'index.html',{'goal':goal,'meal_type':mealtype})
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
def goalform(request):
    if request.method=='POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Goal is created')

            return redirect('goal')
    else:
        form = GoalForm()
        return render(request,'goal_form.html',{'form': form})
def goallist(request):
    goal = Goal.objects.all();
    return  render(request,'goal_list.html',{'table':goal})

def goaldelete(request, value):
    Goal.objects.filter(id=value).delete()
    messages.warning(request, 'Goal is Deleted!')
    return redirect('/goal/list')
def goalupdateform(request, value):
    table = Goal.objects.get(id=value)
    return render(request,'goal_update.html',{'table':table})
def goalupdate(request):
    Goal.objects.filter(id=request.POST.get('id')).update(g_name=request.POST.get('name'),calories=request.POST.get('calories'))
    messages.success(request, 'Goal is Updated!')
    return redirect('/goal/list')

# mealtype
def mealtypeform(request):
    if request.method=='POST':
        form = MealTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Meal type is created')

            return redirect('mealtype')
    else:
        form = MealTypeForm()
        return render(request,'mealtype_form.html',{'form': form})
def mealtypelist(request):
    mealtype = MealType.objects.all();
    return  render(request,'mealtype_list.html',{'table':mealtype})

def mealtypedelete(request, value):
    MealType.objects.filter(id=value).delete()
    messages.warning(request, 'Meal type is Deleted!')
    return redirect('/mealtype/list')
def mealtypeupdateform(request, value):
    table = MealType.objects.get(id=value)
    return render(request,'mealtype_update.html',{'table':table})
def mealtypeupdate(request):
    MealType.objects.filter(id=request.POST.get('id')).update(mt_name=request.POST.get('name'))
    messages.success(request, 'Meal type is Updated!')
    return redirect('/mealtype/list')

# meals

def mealsform(request):
    if request.method=='POST':
            g = Goal.objects.get(id=request.POST.get('goal'))
            m = MealType.objects.get(id=request.POST.get('mealtype'))
            table = Meals.objects.create(goal_id=g,mealtype_id=m,name=request.POST.get('name'),quantity=request.POST.get('quantity'),calories=request.POST.get('calories'),day_time=request.POST.get('day_time'))
            messages.success(request,'Meal is created')
            return redirect('meals')
    else:
        goal = Goal.objects.all()
        mealtype=MealType.objects.all()
        return render(request,'meals_form.html',{'goal':goal,'mealtype':mealtype})
def mealslist(request):
    meals = Meals.objects.select_related('goal_id','mealtype_id')


    return  render(request,'meals_list.html',{'table':meals})

def mealsdelete(request, value):
    Meals.objects.filter(id=value).delete()
    messages.warning(request, 'Meals is Deleted!')
    return redirect('/meals/list')
def mealsupdateform(request, value):
    table = Meals.objects.get(id=value)
    return render(request,'meals_update.html',{'table':table})
def mealsupdate(request):
    Meals.objects.filter(id=request.POST.get('id')).update(name=request.POST.get('name'),quantity=request.POST.get('quantity'),calories=request.POST.get('calories'),day_time=request.POST.get('day_time'))
    messages.success(request, 'Meal is Updated!')
    return redirect('/meals/list')

# supplemets

def supplementsform(request):
    if request.method=='POST':
            g = Goal.objects.get(id=request.POST.get('goal'))

            table = Supplements.objects.create(goal_id=g,name=request.POST.get('name'),day_time=request.POST.get('day_time'))
            messages.success(request,'Supplement is created')
            return redirect('supplements')
    else:
        goal = Goal.objects.all()
        mealtype=MealType.objects.all()
        return render(request,'supplements_form.html',{'goal':goal})
def supplementslist(request):
    supplements = Supplements.objects.select_related('goal_id')


    return  render(request,'supplements_list.html',{'table':supplements})

def supplementsdelete(request, value):
    Supplements.objects.filter(id=value).delete()
    messages.warning(request, 'Supplement is Deleted!')
    return redirect('/supplements/list')
def supplementsupdateform(request, value):
    table = Supplements.objects.get(id=value)
    return render(request,'supplements_update.html',{'table':table})
def supplementsupdate(request):
    Supplements.objects.filter(id=request.POST.get('id')).update(name=request.POST.get('name'),day_time=request.POST.get('day_time'))
    messages.success(request, 'Supplement is Updated!')
    return redirect('/supplements/list')

# home_workout

def home_workoutform(request):
    if request.method=='POST':
            g = Goal.objects.get(id=request.POST.get('goal'))

            table = Homeworkout.objects.create(goal_id=g,name=request.POST.get('name'),sets=request.POST.get('sets'),reps=request.POST.get('reps'))
            messages.success(request,'Home_workout is created')
            return redirect('home_workout')
    else:
        goal = Goal.objects.all()
        mealtype=MealType.objects.all()
        return render(request,'home_workout_form.html',{'goal':goal})
def home_workoutlist(request):
    supplements = Homeworkout.objects.select_related('goal_id')


    return  render(request,'home_workout_list.html',{'table':supplements})

def home_workoutdelete(request, value):
    Homeworkout.objects.filter(id=value).delete()
    messages.warning(request, 'Home_workout is Deleted!')
    return redirect('/home_workout/list')
def home_workoutupdateform(request, value):
    table = Homeworkout.objects.get(id=value)
    return render(request,'home_workout_update.html',{'table':table})
def home_workoutupdate(request):
    Homeworkout.objects.filter(id=request.POST.get('id')).update(name=request.POST.get('name'),sets=request.POST.get('sets'),reps=request.POST.get('reps'))
    messages.success(request, 'Home_workout is Updated!')
    return redirect('/home_workout/list')