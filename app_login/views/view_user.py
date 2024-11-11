from django.shortcuts import render, redirect
from app_login.models import User

def home(request):
    users = {
        'users': User.objects.all()
    }

    return render(request, 'users/home.html', users)

def register(request):
    # TO DO
    # login_id será o Id primary key da Tabela Login
    
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        if user_name and user_email:
            user = User()
            user.name = user_name
            user.email = user_email
            user.login_id = 1
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