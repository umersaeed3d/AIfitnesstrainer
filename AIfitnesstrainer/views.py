from django.shortcuts import render,redirect
from django.contrib import messages
from pprint import  pprint
from django.contrib.auth import login, authenticate
from AIfitnesstrainer.forms import SignUpForm,GoalForm,MealTypeForm
from AIfitnesstrainer.models import Goal
from AIfitnesstrainer.models import MealType
from AIfitnesstrainer.models import Meals
from AIfitnesstrainer.models import Supplements,Homeworkout,Order
from django.http import JsonResponse
import random
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
import ast
import pickle as pk
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from django.contrib.staticfiles.storage import staticfiles_storage
import numpy

bf= 0
lu = 0
prw = 0
pow = 0
d = 0
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

# workoutplan

def generateworkoutplan(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        goal_id = request.POST.get('goal')
        sp = goal_id.split(',')
        if type == '0' :
            age = request.POST.get('age')
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            hw = Homeworkout.objects.select_related('goal_id').filter(goal_id=sp[1])
            listh = []
            j=1
            for i in range(0,len(hw),2):
                listh.append([j,hw[i].name,hw[i].sets,hw[i].reps])
                j=j+1
            s=[]
            supplement = Supplements.objects.select_related('goal_id').filter(goal_id=sp[1])
            for i in supplement:
                s.append([i.name,i.day_time])

            table = Order.objects.create(user_id=request.user.id, type=type, age=age, height=height, weight=weight,
                                         table=listh, supplementtable=s)
            return render(request,'home_workout_plan.html',{'table':listh,'supplement':s})
        else:
            age = request.POST.get('age')
            height = request.POST.get('height')
            weight =request.POST.get('weight')
            goal = sp[0]

            data = [int(age),int(weight),float(height),int(goal)]

            load_model_1 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_1.sav'), 'rb'))
            load_model_2 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_2.sav'), 'rb'))
            load_model_3 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_3.sav'), 'rb'))
            load_model_4 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_4.sav'), 'rb'))
            load_model_5 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_5.sav'), 'rb'))
            load_model_6 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_6.sav'), 'rb'))
            load_model_7 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_7.sav'), 'rb'))
            load_model_8 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_8.sav'), 'rb'))
            load_model_9 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_9.sav'), 'rb'))
            load_model_10 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_10.sav'), 'rb'))
            load_model_11 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_11.sav'), 'rb'))
            load_model_12 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_12.sav'), 'rb'))
            load_model_13 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_13.sav'), 'rb'))
            load_model_14 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_14.sav'), 'rb'))
            load_model_15 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_15.sav'), 'rb'))
            load_model_16 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_16.sav'), 'rb'))
            load_model_17 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_17.sav'), 'rb'))
            load_model_18 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_18.sav'), 'rb'))
            load_model_19 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_19.sav'), 'rb'))
            load_model_20 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_20.sav'), 'rb'))
            load_model_21 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_21.sav'), 'rb'))
            load_model_22 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_22.sav'), 'rb'))
            load_model_23 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_23.sav'), 'rb'))
            load_model_24 = pk.load(open(staticfiles_storage.path('frontend/exmodel/finalized_model_24.sav'), 'rb'))

            d_workout = pd.read_csv(staticfiles_storage.path('frontend/exmodel/workout.csv'))

            listw = []
            a = numpy.array(data)

            z= load_model_1.predict([a])
            listw.append(['Straight Bench Press',z])
            Z = load_model_2.predict([a])
            listw.append(['Decline Bench Press',Z])
            X = load_model_3.predict([a])
            listw.append(['Dumbell Flyes',X])
            x = load_model_4.predict([a])
            listw.append(['Front Barbell Press',x])
            y = load_model_5.predict([a])
            listw.append(['Side Laterals',y])
            Y = load_model_6.predict([a])
            listw.append(['Rear Delt Flyes',Y])
            o = load_model_7.predict([a])
            listw.append(['Face Pulls',o])
            O = load_model_8.predict([a])
            listw.append(['Dumbell Shrugs',O])
            p = load_model_9.predict([a])
            listw.append(['Deadlift',p])
            P = load_model_10.predict([a])
            listw.append(['Bentover Barbell Rows',P])
            q = load_model_11.predict([a])
            listw.append(['T-bar Rows',q])
            Q = load_model_12.predict([a])
            listw.append(['Front Cable Pull Down',Q])
            r = load_model_13.predict([a])
            listw.append(['Back Cable Pull Down',r])
            R = load_model_14.predict([a])
            listw.append(['Barbell Curls',R])
            S = load_model_15.predict([a])
            listw.append(['Hammer Curls',S])
            s = load_model_16.predict([a])
            listw.append(['E-z Bar Curls',s])
            t = load_model_17.predict([a])
            listw.append(['Preacher Curls',t])
            T = load_model_18.predict([a])
            listw.append(['Triceps Dips',T])
            u = load_model_19.predict([a])
            listw.append(['Double Hand Overhead Press',u])
            U = load_model_20.predict([a])
            listw.append(['Skull Crusher',U])
            v = load_model_21.predict([a])
            listw.append(['Squat',v])
            V = load_model_22.predict([a])
            listw.append(['Dumbell Lunges',V])
            W = load_model_23.predict([a])
            listw.append(['Leg Press',W])
            w = load_model_24.predict([a])
            listw.append(['Lying Leg Curls',w])

            Smodel_1 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_1.sav'), 'rb'))
            Smodel_2 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_2.sav'), 'rb'))
            Smodel_3 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_3.sav'), 'rb'))
            Smodel_4 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_4.sav'), 'rb'))
            Smodel_5 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_5.sav'), 'rb'))
            Smodel_6 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_6.sav'), 'rb'))
            Smodel_7 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_7.sav'), 'rb'))
            Smodel_8 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_8.sav'), 'rb'))
            Smodel_9 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_9.sav'), 'rb'))
            Smodel_10 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_10.sav'), 'rb'))
            Smodel_11 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_11.sav'), 'rb'))
            Smodel_12 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_12.sav'), 'rb'))
            Smodel_13 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_13.sav'), 'rb'))
            Smodel_14 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_14.sav'), 'rb'))
            Smodel_15 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_15.sav'), 'rb'))
            Smodel_16 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_16.sav'), 'rb'))
            Smodel_17 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_17.sav'), 'rb'))
            Smodel_18 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_18.sav'), 'rb'))
            Smodel_19 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_19.sav'), 'rb'))
            Smodel_20 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_20.sav'), 'rb'))
            Smodel_21 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_21.sav'), 'rb'))
            Smodel_22 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_22.sav'), 'rb'))
            Smodel_23 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_23.sav'), 'rb'))
            Smodel_24 = pk.load(open(staticfiles_storage.path('frontend/srmodel/model_24.sav'), 'rb'))

            # load model dict from disk
            with open(staticfiles_storage.path('frontend/srmodel/model_1.pickle'), 'rb') as handle:
                Tdict_1 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_2.pickle'), 'rb') as handle:
                Tdict_2 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_3.pickle'), 'rb') as handle:
                Tdict_3 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_4.pickle'), 'rb') as handle:
                Tdict_4 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_5.pickle'), 'rb') as handle:
                Tdict_5 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_6.pickle'), 'rb') as handle:
                Tdict_6 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_7.pickle'), 'rb') as handle:
                Tdict_7 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_8.pickle'), 'rb') as handle:
                Tdict_8 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_9.pickle'), 'rb') as handle:
                Tdict_9 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_10.pickle'), 'rb') as handle:
                Tdict_10 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_11.pickle'), 'rb') as handle:
                Tdict_11 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_12.pickle'), 'rb') as handle:
                Tdict_12 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_13.pickle'), 'rb') as handle:
                Tdict_13 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_14.pickle'), 'rb') as handle:
                Tdict_14 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_15.pickle'), 'rb') as handle:
                Tdict_15 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_16.pickle'), 'rb') as handle:
                Tdict_16 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_17.pickle'), 'rb') as handle:
                Tdict_17 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_18.pickle'), 'rb') as handle:
                Tdict_18 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_19.pickle'), 'rb') as handle:
                Tdict_19 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_20.pickle'), 'rb') as handle:
                Tdict_20 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_21.pickle'), 'rb') as handle:
                Tdict_21 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_22.pickle'), 'rb') as handle:
                Tdict_22 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_23.pickle'), 'rb') as handle:
                Tdict_23 = pk.load(handle)
            with open(staticfiles_storage.path('frontend/srmodel/model_24.pickle'), 'rb') as handle:
                Tdict_24 = pk.load(handle)


            sr_workout = pd.read_csv(staticfiles_storage.path('frontend/srmodel/sets and reps.csv'))

            res = Smodel_1.predict([a])
            key_list = list(Tdict_1.keys())
            val_list = list(Tdict_1.values())
            listw[0].append(key_list[val_list.index(res)])

            res = Smodel_2.predict([a])
            key_list = list(Tdict_2.keys())
            val_list = list(Tdict_2.values())
            listw[1].append(key_list[val_list.index(res)])

            res = Smodel_3.predict([a])
            key_list = list(Tdict_3.keys())
            val_list = list(Tdict_3.values())
            listw[2].append(key_list[val_list.index(res)])

            res = Smodel_4.predict([a])
            key_list = list(Tdict_4.keys())
            val_list = list(Tdict_4.values())
            listw[3].append(key_list[val_list.index(res)])

            res = Smodel_5.predict([a])
            key_list = list(Tdict_5.keys())
            val_list = list(Tdict_5.values())
            listw[4].append(key_list[val_list.index(res)])

            res = Smodel_6.predict([a])
            key_list = list(Tdict_6.keys())
            val_list = list(Tdict_6.values())
            listw[5].append(key_list[val_list.index(res)])

            res = Smodel_7.predict([a])
            key_list = list(Tdict_7.keys())
            val_list = list(Tdict_7.values())
            listw[6].append(key_list[val_list.index(res)])

            res = Smodel_8.predict([a])
            key_list = list(Tdict_8.keys())
            val_list = list(Tdict_8.values())
            listw[7].append(key_list[val_list.index(res)])

            res = Smodel_9.predict([a])
            key_list = list(Tdict_9.keys())
            val_list = list(Tdict_9.values())
            listw[8].append(key_list[val_list.index(res)])

            res = Smodel_10.predict([a])
            key_list = list(Tdict_10.keys())
            val_list = list(Tdict_10.values())
            listw[9].append(key_list[val_list.index(res)])

            res = Smodel_11.predict([a])
            key_list = list(Tdict_11.keys())
            val_list = list(Tdict_11.values())
            listw[10].append(key_list[val_list.index(res)])

            res = Smodel_12.predict([a])
            key_list = list(Tdict_12.keys())
            val_list = list(Tdict_12.values())
            listw[11].append(key_list[val_list.index(res)])

            res = Smodel_13.predict([a])
            key_list = list(Tdict_13.keys())
            val_list = list(Tdict_13.values())
            listw[12].append(key_list[val_list.index(res)])

            res = Smodel_14.predict([a])
            key_list = list(Tdict_14.keys())
            val_list = list(Tdict_14.values())
            listw[13].append(key_list[val_list.index(res)])

            res = Smodel_15.predict([a])
            key_list = list(Tdict_15.keys())
            val_list = list(Tdict_15.values())
            listw[14].append(key_list[val_list.index(res)])

            res = Smodel_16.predict([a])
            key_list = list(Tdict_16.keys())
            val_list = list(Tdict_16.values())
            listw[15].append(key_list[val_list.index(res)])

            res = Smodel_17.predict([a])
            key_list = list(Tdict_17.keys())
            val_list = list(Tdict_17.values())
            listw[16].append(key_list[val_list.index(res)])

            res = Smodel_18.predict([a])
            key_list = list(Tdict_18.keys())
            val_list = list(Tdict_18.values())
            listw[17].append(key_list[val_list.index(res)])

            res = Smodel_19.predict([a])
            key_list = list(Tdict_19.keys())
            val_list = list(Tdict_19.values())
            listw[18].append(key_list[val_list.index(res)])

            res = Smodel_20.predict([a])
            key_list = list(Tdict_20.keys())
            val_list = list(Tdict_20.values())
            listw[19].append(key_list[val_list.index(res)])

            res = Smodel_21.predict([a])
            key_list = list(Tdict_21.keys())
            val_list = list(Tdict_21.values())
            listw[20].append(key_list[val_list.index(res)])

            res = Smodel_22.predict([a])
            key_list = list(Tdict_22.keys())
            val_list = list(Tdict_22.values())
            listw[21].append(key_list[val_list.index(res)])

            res = Smodel_23.predict([a])
            key_list = list(Tdict_23.keys())
            val_list = list(Tdict_23.values())
            listw[22].append(key_list[val_list.index(res)])

            res = Smodel_24.predict([a])
            key_list = list(Tdict_24.keys())
            val_list = list(Tdict_24.values())
            listw[23].append(key_list[val_list.index(res)])
            print(len(listw))
            i=0
            for k in listw:
                for j in k:
                    if j == 0:
                        del listw[i:i+1]
                i = i+1
            count = len(listw)
            div  = int(count/3)

            for z in range(0,len(listw)):
                if z in range(0,(int(len(listw)/3))):
                    listw[z].append('Day 1')
                elif z in range(div,(int(len(listw)/2))+1):
                    listw[z].append('Day 2')
                else:
                    listw[z].append('Day 3')
            i=0
            for j in listw:
                l=0
                for k in j:
                    if k == [1]:
                        del listw[i][l:l+1]
                    elif k == [0]:
                        del listw[i][l:l+1]
                    l = l + 1
                i = i + 1
            print(listw)
            purelist = []
            for j in listw:
                for k in j:
                    if k == 'Day 1':
                        purelist.append(j)
            for j in listw:
                for k in j:
                    if k == 'Day 2':
                        purelist.append(j)
            for j in listw:
                for k in j:
                    if k == 'Day 3':
                        purelist.append(j)
            print(sp[1])
            s = []
            supplement = Supplements.objects.select_related('goal_id').filter(goal_id=sp[1])
            for i in supplement:
                s.append([i.name, i.day_time])
            table = Order.objects.create(user_id=request.user.id,type=type,age=age,height=height,weight=weight,table=purelist,supplementtable=s)
            return render(request,'gym_workout_plan.html',{'table':purelist,'supplement':s})

    else:
        return redirect('/')

def generatedietplan(request):
    if request.method == 'POST':
        global bf
        global lu
        global prw
        global pow
        global d
        type = request.POST.get('type')
        mtype = request.POST.get('meal_type')
        goal = request.POST.get('goal')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')

        dp = Meals.objects.select_related('goal_id','mealtype_id').filter(goal_id=goal,mealtype_id=mtype)
        list = []
        j=1

        breakfast = 0
        lunch = 0
        pre_workout = 0
        post_workout = 0
        dinner = 0
        total_cal = 0
        cal = dp[0].goal_id.calories

        if cal == '1500':
            bf = 250
            lu = 500
            prw = 150
            pow = 150
            d = 450


        elif cal == '2000':
            bf = 400
            lu = 500
            prw = 200
            pow = 400
            d = 500
        elif cal == '3000':
            bf = 600
            lu = 800
            prw = 300
            pow = 500

            d = 800
        checkrandom = []

        for i in range(0,len(dp)):

            r = random.randint(0,len(dp)-1)
            if r not in checkrandom:
                checkrandom.append(r)
            else:
                continue

            if total_cal < int(dp[i].goal_id.calories):



                if dp[r].day_time == '0' and breakfast < bf:
                    print('bf')
                    list.append([dp[r].name,dp[r].quantity,dp[r].calories,'Breakfast'])
                    breakfast = breakfast + int(dp[r].calories)
                if dp[r].day_time == '1' and lunch < lu:
                    print('lunch')
                    list.append([dp[r].name,dp[r].quantity,dp[r].calories,'Lunch'])
                    lunch = lunch + int(dp[r].calories)
                    total_cal = total_cal + int(dp[r].calories)
                if dp[r].day_time == '2' and pre_workout < prw:
                    print('preworkout')
                    list.append([dp[r].name,dp[r].quantity,dp[r].calories,'Pre-Workout'])
                    pre_workout = pre_workout + int(dp[r].calories)
                    total_cal = total_cal + int(dp[r].calories)
                if dp[r].day_time == '3' and post_workout < pow:
                    print('postworlpit')
                    list.append([dp[r].name,dp[r].quantity,dp[r].calories,'Post-Workout'])
                    post_workout = post_workout + int(dp[r].calories)
                    total_cal = total_cal + int(dp[r].calories)
                if dp[r].day_time == '4' and dinner < d:
                    print('dinner')
                    list.append([dp[r].name,dp[r].quantity,dp[r].calories,'Dinner'])
                    dinner = dinner + int(dp[r].calories)
                    total_cal = total_cal + int(dp[r].calories)
                j = j+ 1
            else:
                break
        print(total_cal)

        supplement = Supplements.objects.select_related('goal_id').filter(goal_id=goal)
        s = []

        for i in supplement:
            s.append([i.name, i.day_time])
        table = Order.objects.create(user_id=request.user.id, type=type, age=age, height=height, weight=weight,
                                     table=list, supplementtable=s)
        return render(request,'diet_plan.html',{'table':list,'supplement':s})
    else:
        return redirect('/')

def orders(request):
    table = Order.objects.filter(user_id=request.user.id)
    return render(request,'orders.html',{'table':table})

def ordersbyid(request,value):
    table = Order.objects.get(id=value)
    t = table.table
    st = table.supplementtable
    type = table.type
    s=ast.literal_eval(t)
    sp = ast.literal_eval(st)


    if type == '0':
        return  render(request,'home_workout_plan.html',{'table':s})
    elif type == '1':
        return render(request, 'gym_workout_plan.html', {'table': s,'supplement':sp})
    else:
        return render(request, 'diet_plan.html', {'table': s,'supplement':sp})
