from django.shortcuts import render, redirect
from app_login.models import Login
from app_login.views import view_user
from app_login.util import LoginUtil
from app_login.util.LoginUtil import *

def login(request):
    return render(request, 'login/index.html')

def validate_login(request):
    
    if request.method == 'POST':
        login_email = request.POST.get('login_email')
        login_password = request.POST.get('login_password')
        
        if not login_email or not login_password:
            # TO DO
            # Criar Mensagens de erro para Página
            # Criar redirect com parametros para passar mensagem para página
            # https://stackoverflow.com/questions/3209906/django-return-redirect-with-parameters
            return redirect('login')
        
        login = Login()
        query_set = Login.objects.filter(email=login_email)
        if not query_set:
            return render(request, 'login/index.html')

        login = query_set.first()
        enconded_pass = LoginUtil.generate_password_hash(login_password, login.random_hash)
        if login.password != enconded_pass:
            return render(request, 'login/index.html')
            
        # login validado                
        # TO DO
        # salvar dados do Usuario em Session / Cookie
        return redirect(view_user.home)
    
    return render(request, 'login/index.html')
