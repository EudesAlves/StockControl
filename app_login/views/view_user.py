from django.shortcuts import render, redirect
from app_login.models import User
from app_login.models import Login
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *


def user_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    users = {
        'users': User.objects.filter(active=True)
    }

    return render(request, 'users/index.html', users)

def user_register(request):
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

def user_update(request, id):
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

        success_message = "Usuário " +form['name']+ " atualizado com sucesso."
        return render(request, 'users/update.html', {'success_message' : success_message, 'user' : form})

def user_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        user = User.objects.get(id=id)
        return render(request, "users/delete.html", {"user": user})
    
    if request.method == 'POST':
        form = {}
        if id:
            user = User.objects.get(id=id)
            form['id'] = user.id
            form['name'] = user.name
            form['email'] = user.email

            user.active = False
            user.save()

            delete_login(user.login_id)

        success_message = "Usuário " +form['name']+ " excluído com sucesso."
        return render(request, 'users/delete.html', {'success_message' : success_message, 'user' : form})

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

def delete_login(login_id):
    login = Login.objects.get(id=login_id)
    login.active = False
    login.save()