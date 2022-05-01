
from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    path('',views.index,name='index') ,
    path('about/',views.about,name='about') ,
    path('contact/',views.contact,name='contact'),

    path('login/',views.userlogin,name='login'),
    
    
    path('signup/',views.signup1,name="signup"),
    path('logout/',views.Logout,name="logout"),
    
]
