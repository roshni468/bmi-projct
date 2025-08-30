from django.shortcuts import render,redirect,get_object_or_404
from lima_20_Calorycounter.views import*
from caloryApp.models import*
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from caloryApp.forms import*
from datetime import date
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum


def signin_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_Password')
        email = request.POST.get('email')

        
     
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signin_page')

        if CustomModel.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signin_page')

      
        auth_user = CustomModel.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        if auth_user:

            UserProfile.objects.create(
                user=auth_user
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login_page')

    return render(request, 'signin.html')
# login

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home_page')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_page')

    return render(request, 'login.html')


# log out
def log_out(request):
    logout(request)
    return redirect("login_page")


# change pasword
def change_pass(request):
    current_user=request.user
    if request.method == 'POST':
        current_password = request.POST.get("current_password")
        confirm_password = request.POST.get("confirm_password")
        new_password = request.POST.get("new_password")
        
        if check_password(current_password, request.user.password):

           
            if new_password == confirm_password:
                current_user.set_password(new_password)  
                current_user.save()
                update_session_auth_hash(request, current_user)
                return redirect("login_page")

    return render(request, "change_pass.html")


# home_page
def home_page(request):
    current_user = request.user
    today = date.today()

    calori_entry_item = CalorieEntryModel.objects.all()
    total_calori_data = totalCalorieModel.objects.all()

    # Set default values
    weight = height = age = BMR = 0
    gender = ''
    
    # Safely get user profile
    profile = getattr(current_user, 'profile_user', None)
    
    if profile:
        weight = profile.weight_kg
        height = profile.height_cm
        age = profile.age
        gender = profile.gender

        if weight and height and age:
            if gender.lower() == 'male':
                BMR = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
            else:
                BMR = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

    BMR = round(BMR, 2)

    # Fetch today's calorie entries
    today_calori_comsum = CalorieEntryModel.objects.filter(user=current_user, date=today)
    total_consumed = today_calori_comsum.aggregate(total=Sum('calories_consumed'))['total'] or 0

    remainig = round(BMR - total_consumed, 2)

    context = {
        'calori_entry_item': calori_entry_item,
        'total_calori_data': total_calori_data,
        'BMR': BMR,
        'today_calori_comsum': today_calori_comsum,
        'remainig': remainig,
        'total_consumed': total_consumed,
    }
    return render(request,"home.html",context)




# profile
def profile_page(request):

    return render(request,"profile.html")

# update_profile
def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_page')  
    else:
        form = UserProfileForm(instance=profile)
    return render(request,"update_profile.html" , {'form': form})


# add calory
def add_calori(request):
    if request.method == 'POST':
        calori_form = CalorieEntryForm(request.POST)
        current_date = date.today()
        if calori_form.is_valid():
            calori_form = calori_form.save(commit=False)
            calori_form.user = request.user
            calori_form.save()
        
        today_calories = totalCalorieModel.objects.filter(user=request.user, date=current_date).first()
        if today_calories:
                today_calories.total_Calorie += calori_form.calories_consumed
                today_calories.save()
        else:
            totalCalorieModel.objects.create(
                user = request.user,
                total_Calorie = calori_form.calories_consumed,
            )
            return redirect('home_page')
    
    else:
        calori_form = CalorieEntryForm()

    return render(request,"add_calori.html" , {'calori_form': calori_form})






def update_calorie(request, id):
    entry = CalorieEntryModel.objects.get(id=id)
    if request.method == 'POST':
        form = CalorieEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form = CalorieEntryForm(instance=entry)
    return render(request, 'update_calorie.html', {'form': form})
    

def delete_calorie(request, id):
    CalorieEntryModel.objects.filter(id=id).delete()
    return redirect('home_page')