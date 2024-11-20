from django.shortcuts import render, redirect
from app_login.models import User
from app_login.models import Login
from app_login.util import LoginUtil
from app_login.util.LoginUtil import *

def home(request):
    users = {
        'users': User.objects.all()
    }

    return render(request, 'users/home.html', users)

def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        login_password = request.POST.get('login_password')
        login_password_confirm = request.POST.get('login_password_confirm')
        
        if user_name and user_email and login_password and login_password_confirm:
            user = User()
            login = Login()

            random_hash = LoginUtil.generate_random_hash()
            login.email = user_email
            login.random_hash = random_hash
            login.password = LoginUtil.generate_password_hash(login_password, random_hash)
            login.save()
            login_id = (Login.objects.last()).id

            user.name = user_name
            user.email = user_email
            user.login_id = login_id
            user.save()

    # Get registered users
    users = {
        'users': User.objects.all()
    }

    # Return data to page
    return render(request, 'users/register.html', users)

def update(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        return render(request, "users/update.html", {"user": user})
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        if user_name and user_email:
            user = User.objects.get(id=id)
            user.name = user_name
            user.email = user_email
            user.save()

        return redirect(home)

def delete(request, id):
    if request.method == 'GET':
        user = User.objects.get(id=id)
        return render(request, "users/delete.html", {"user": user})
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            user.delete()

        return redirect(home)
