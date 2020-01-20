from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from AIfitnesstrainer.models import Goal,Meals,MealType,Supplements


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class GoalForm(forms.ModelForm):
    g_name = forms.CharField(label='Goal Name', max_length=100)
    calories = forms.IntegerField(label='Calories')
    class Meta:
        model = Goal
        fields = ('g_name','calories', )

class MealTypeForm(forms.ModelForm):
    mt_name = forms.CharField(label='Meal Type Name', max_length=100)
    class Meta:
        model = MealType
        fields = ('mt_name', )