from django import forms
from .models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [ 'name','age', 'gender', 'height_cm', 'weight_kg']



class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieEntryModel
        fields = [ 'item_name','calories_consumed']