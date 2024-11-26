from django.shortcuts import render, redirect
from app_login.models import User
from app_login.models import Login
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *


def home(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    users = {
        'users': User.objects.all()
    }

    return render(request, 'users/home.html', users)

def register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('user_name')
        form['email'] = request.POST.get('user_email')
        form['password'] = request.POST.get('login_password')
        form['password_confirm'] = request.POST.get('login_password_confirm')

        message.messages = validate_user(form)
        
        if message.messages:
            return render(request, 'users/register.html', {'messages' : message.messages, 'user' : form})
        
        login = Login()
        user = User()
        random_hash = LoginUtil.generate_random_hash()
        login.email = form['email']
        login.random_hash = random_hash
        login.password = LoginUtil.generate_password_hash(form['password'], random_hash)
        login.save()
        login_id = (Login.objects.last()).id

        user.name = form['name']
        user.email = form['email']
        user.login_id = login_id
        user.save()

        success_message = "Usuário " +form['name']+ " cadastrado com sucesso."
        return render(request, 'users/register.html', {'success_message' : success_message})

    return render(request, 'users/register.html')

def update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        user = User.objects.get(id=id)
        return render(request, "users/update.html", {"user": user})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('user_name')
        form['email'] = request.POST.get('user_email')
        if not form['name'] or not form['email']:
            message = MessageAlert()
            error = "Todos os campos devem ser preenchidos"
            message.add(error)
            return render(request, 'users/update.html', {'messages' : message.messages, 'user' : form})

        user = User.objects.get(id=id)
        user.name = form['name']
        user.email = form['email']
        user.save()

        return redirect(home)

def delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        user = User.objects.get(id=id)
        return render(request, "users/delete.html", {"user": user})
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            user.delete()

        return redirect(home)

def validate_user(user):
    message = MessageAlert()
    if not user['name'] or not user['email'] or not user['password'] or not user['password_confirm']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    query_set = User.objects.filter(email=user['email'])
    if query_set:
        error_text = "Email já cadastrado no Sistema"
        message.add(error_text)

    if user['password'] != user['password_confirm']:
            error_text = "Campos Senha e Confirmar Senha devem ser iguais"
            message.add(error_text)

    return message.messages
