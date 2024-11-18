from django.shortcuts import render, redirect
from app_login.models import Login

def login(request):
    return render(request, 'login/index.html')

def validate_login(request):
    if request.method == 'POST':
        login_email = request.POST.get('login_email')
        login_password = request.POST.get('login_password')
        
        if login_email and login_password:
            login = Login()

        # TO DO
        # Alterar campo user para email, no model Login
        # Salvar email na tabela Login no registro de usuário
        # Fazer validação de senha baseado no login email
    
    return render(request, 'login/index.html')