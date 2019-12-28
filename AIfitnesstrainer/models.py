from django.db import models

class Goal(models.Model):
    id = models.CharField(max_length=11,primary_key=True)
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'goal'
class MealType(models.Model):
    id = models.CharField(max_length=11,primary_key=True)
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'meal_type'
class Meals(models.Model):
    id = models.CharField(max_length=11,primary_key=True)
    goal_id = models.CharField(max_length=11)
    mealtype_id = models.CharField(max_length=11)
    name = models.CharField(max_length=225)
    quantity = models.CharField(max_length=225)
    day_time = models.CharField(max_length=225)
    class Meta:
        db_table = 'meals'
class Supplements(models.Model):
    id = models.CharField(max_length=11,primary_key=True)
    goal_id = models.CharField(max_length=11)
    name = models.CharField(max_length=225)
    day_time = models.CharField(max_length=225)
    class Meta:
        db_table = 'supplements'


