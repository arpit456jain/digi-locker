from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db import IntegrityError
from django.contrib import messages


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    context = {'auth': request.user.is_authenticated}
    return render(request, 'home.html', context)

def about(request):
    return redirect('/#about')

def contact(request):
    return "contact"

def signup1(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        contact = request.POST['contact']
        role = request.POST['role']
        dept = request.POST['dept']
        try:
            user = User.objects.create_user(username=email, password=password, first_name=fname, last_name=lname)
            user.is_active = False
            user.save()
            signup = Signup.objects.create(user=user, contact=contact, branch=dept, role=role)
            signup.save()
            
        except IntegrityError:
            messages.info(request, "Username taken, Try different")
            return render(request, "signup.html")
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'signup.html')

def Logout(request):
    try:
        for i in OTPModel.objects.filter(user=request.user.username):
            i.delete()
    except:
        pass
    finally:
        logout(request)
        return redirect('index')

def userlogin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            u = request.POST['username']
            p = request.POST['password']
            try:
                user = auth.authenticate(username=u, password=p)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, 'Username of password wrong')
                    return redirect('login')
            except :
                print("some error occured login again")
                return("please login..")
        else:
            return HttpResponse("please login..")

    else:
        return redirect('index')