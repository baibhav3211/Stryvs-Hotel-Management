from django.shortcuts import render, redirect   
from django.contrib import auth, messages
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=="POST":
        first_name = request.POST["cust_name"]
        email = request.POST["cust_email"]
        mobile = request.POST["cust_mobile"]
        username = request.POST["username"]
        password = request.POST["password"]
        cnfpassword = request.POST["cnfpassword"]
        if password!=cnfpassword:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Passwords Not Same')
            return redirect('/')
        if User.objects.filter(username=username).exists():
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Username Already Taken')
            return redirect('/')
        password=make_password(password,hasher='default')
        obj = User.objects.create(first_name=first_name,email=email,mobile=mobile,username=username,password=password)
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'You have Successfully Registered in the portal')
        return redirect('/')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        obj = authenticate(username = username,password = password)
        if obj is not None:
            auth.login(request,obj)
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Login Successful')
            return redirect('/dashboard')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'Username / Password not correct. Recheck and Login')
            return redirect('/')



def logout(request):
    auth.logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'Logout Successful. Thanks for using the Service')
    return redirect('/')