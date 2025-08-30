"""
URL configuration for lima_20_Calorycounter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lima_20_Calorycounter.views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login_page, name="login_page"),
    path('signin_page',signin_page, name="signin_page"),
    path('log_out',log_out, name="log_out"),
    path('change_pass',change_pass, name="change_pass"),
    path('home_page',home_page, name="home_page"),
    path('profile_page',profile_page, name="profile_page"),
    path('update_profile',update_profile, name="update_profile"),
    path('add_calori',add_calori, name="add_calori"),
    path('delete_calorie/delete/<int:id>/', delete_calorie, name='delete_calorie'),
    path('update_calorie/edit/<int:id>/', update_calorie, name='update_calorie'),


]
