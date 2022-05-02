
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from home import views
urlpatterns = [
    path('',views.index,name='index') ,
    path('about/',views.about,name='about') ,
    path('contact/',views.contact,name='contact'),

    path('login/',views.userlogin,name='login'),
    
    
    path('signup/',views.signup1,name="signup"),
    path('logout/',views.Logout,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),

    path('upload_notes/',views.upload_notes,name="upload_notes"),
    path('view_usernotes/<str:type>',views.view_usernotes,name="view_usernotes"),
    path('viewall_usernotes/',views.viewall_usernotes,name="viewall_usernotes"),
    path('note/<int:id>', views.view_note, name="view_note"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
