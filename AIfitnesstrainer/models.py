from django.db import models

class Goal(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    g_name = models.CharField(max_length=20)
    calories = models.CharField(max_length=20)
    class Meta:
        db_table = 'goal'
class MealType(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    mt_name = models.CharField(max_length=20)
    class Meta:
        db_table = 'meal_type'
class Meals(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    goal_id = models.ForeignKey(Goal,on_delete=models.CASCADE, null=True)
    mealtype_id = models.ForeignKey(MealType,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=225)
    quantity = models.CharField(max_length=225)
    calories = models.CharField(max_length=225)
    day_time = models.CharField(max_length=225)
    class Meta:
        db_table = 'meals'
class Supplements(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    goal_id = models.ForeignKey(Goal,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=225)
    day_time = models.CharField(max_length=225)
    class Meta:
        db_table = 'supplements'
class Homeworkout(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    goal_id = models.ForeignKey(Goal,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=225)
    sets = models.IntegerField(max_length=11)
    reps = models.IntegerField(max_length=11)
    class Meta:
        db_table = 'home_workout'

class Order(models.Model):
    id = models.AutoField(max_length=11,primary_key=True)
    user_id = models.IntegerField(max_length=11)
    type = models.CharField(max_length=255)

    age = models.CharField(max_length=225)
    height = models.CharField(max_length=11)
    weight = models.CharField(max_length=11)
    table = models.CharField(max_length=2000)
    supplementtable = models.CharField(max_length=2000)
    class Meta:
        db_table = 'order'

