from django.shortcuts import render, redirect
from app_login.models import Login
from app_login.models import User
from app_login.views import view_user
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *

def login(request):
    populate_initial_data(request)

    return render(request, 'login/index.html')

def validate_login(request):
    message = MessageAlert()
    if request.method == 'POST':
        login_email = request.POST.get('login_email')
        login_password = request.POST.get('login_password')
        if not login_email or not login_password:
            error_text = "Campos Email e Senha devem ser preenchidos"
            message.add(error_text)

            return render(request, 'login/index.html', {'messages' : message.messages})
            
        login = Login()
        query_set = Login.objects.filter(email=login_email, active=True)
        if not query_set:
            error_text = "Email não está cadastrado"
            message.add(error_text)
            return render(request, 'login/index.html', {'messages' : message.messages})

        login = query_set.first()
        enconded_pass = LoginUtil.generate_password_hash(login_password, login.random_hash)
        if login.password != enconded_pass:
            error_text = "Senha incorreta para o Email informado"
            message.add(error_text)
            return render(request, 'login/index.html', {'messages' : message.messages})
            

        user = User()
        query_set = User.objects.filter(login_id=login.id)
        user = query_set.first()
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name

        return redirect(view_user.home)
        #return redirect('')
    
    return render(request, 'login/index.html')

def logout(request):
    request.session.clear()
    request.session.aflush()
    return redirect('login')

def populate_initial_data(request):
    if not 'initial_login' in request.session:
        request.session['initial_login'] = 1
        LoginUtil.populate_initial_login()