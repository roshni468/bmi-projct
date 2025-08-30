from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomModel(AbstractUser):

    def __str__(self):
        return self.username
    


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user = models.OneToOneField(CustomModel, on_delete=models.CASCADE, related_name="profile_user",null=True)
    name =models.CharField(max_length=100,null=True)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,null=True)
    height_cm = models.FloatField(null=True)
    weight_kg = models.FloatField(null=True)


    def __str__(self):
        return self.user.username

class CalorieEntryModel(models.Model):
    user = models.ForeignKey(CustomModel, on_delete=models.CASCADE,related_name="calori_count",null=True)
    item_name = models.CharField(max_length=100,null=True)
    calories_consumed = models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_name} - {self.calories_consumed} kcal"

    
    
class totalCalorieModel(models.Model):
    user = models.ForeignKey(CustomModel, on_delete=models.CASCADE,null=True)
    total_Calorie= models.PositiveIntegerField(null=True)
    date = models.DateField(auto_now_add=True)


    
