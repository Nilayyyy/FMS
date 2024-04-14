from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('add-spending', views.add_spending, name='add-spending'),
    path('register', views.register, name='register'),
    path('spendings', views.spendings, name='spendings'),
    path('my-profile', views.my_profile, name='my-profile'),
]