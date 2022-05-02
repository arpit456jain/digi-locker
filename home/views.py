from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login, logout
import datetime
from django.db import IntegrityError
from django.contrib import messages
from django.conf import settings

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('/profile')
    context = {'auth': request.user.is_authenticated}
    return render(request, 'home.html', context)

def about(request):
    return redirect('/#about')



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
    
    if request.method == 'POST':
        print("jfj")
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        exist = User.objects.filter(username=username).exists()
        print(exist)
        if not exist:
            messages.error(request," username not Found Please Sign Up")
            return redirect('/login')
        user = User.objects.filter(username=username).first()
        print(user,user.password,password)
        
        user=authenticate(username=username,password=password) 
        if user is not None:
            login(request, user)
            print("Successfully Logged In")
            print('loged in')
            return redirect("/")
    return render(request,'login.html')

def contact(request):
    print("contb")
    if request.method == 'POST':
        print("contactgbedbh")
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        print(name, email,subject,message)
        ins = Contact(name=name,email=email,subject=subject,message=message)
        ins.save()
        messages.success(request,"thanks for contacting us")
        return redirect("/")
    
    return redirect("/#contact")


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    try:
        data = Signup.objects.get(user=user)
    except Signup.DoesNotExist:
        if user.is_superuser and user.is_staff:
            user.first_name = user.username
            user.save()
            signup = Signup.objects.create(user=user, contact="", branch="", role="")
            signup.save()
            data = Signup.objects.get(user = user)
    d = {'data': data, 'user': user, 'auth': request.user.is_authenticated}
    
    return render(request, 'profile.html', d)

def upload_notes(request):
    if not request.user.is_authenticated:
        messages.info(request, "Login to Upload Notes")
        return redirect('login')
    if request.method == 'POST':
        s = request.POST['subject']
        n = request.FILES['file']
        f = request.POST['ftype']
        d = request.POST['desc']
        u = User.objects.filter(username=request.user.username).first()
        try:
            Notes.objects.create(user=u, uploadingdate=datetime.date.today(), subject=s,
                                 notesfile=n, filetype=f, description=d, status="Pending")
            messages.success(request, f'Notes Uploaded Successfully')
            return redirect('/view_usernotes/open');
        except:
            messages.error(request, f'Something went wrong, Try Again')

    return render(request, 'upload_notes.html', {'auth': request.user.is_authenticated})
def view_users(request):
    pass

def all_notes(request):
    pass

def view_usernotes(request, type):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to access your uploads")
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user=user)
    reviewed = False
    if type == "reviewed":
        notes = notes.exclude(status="Pending")
        reviewed = True
    else:
        notes = notes.filter(status="Pending")
    
    l_pen = len(Notes.objects.filter(user=user, status="Pending"))
    l_rev = len((Notes.objects.filter(user=user)).exclude(status="Pending"))
    d = {'notes': notes, 'self': True, 'reviewed': reviewed, 'l_rev': l_rev, 'l_pen': l_pen }
    return render(request, 'viewall_usernotes.html', d)

def viewall_usernotes(request):
    notes = Notes.objects.filter(status="Accepted")
    d = {'notes': notes, 'viewall': True, 'reviewed': True}
    return render(request, 'viewall_usernotes.html', d)

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login first")
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user=user)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        contact = request.POST['contact']
        user.first_name, user.last_name, data.contact = fname, lname, contact
        user.save()
        data.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('/profile')
    d = {'data': data, 'user': user, 'auth': request.user.is_authenticated}
    return render(request, 'edit_profile.html', d)

def view_note(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        note = Notes.objects.get(id=id)
        
        d = {'note': note}
        return render(request, "view_note.html", d)
    except:
        return HttpResponse("Resource you're looking for is not available now")
