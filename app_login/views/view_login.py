from django.shortcuts import render, redirect
from app_login.models import Login

def login(request):
    return render(request, 'login/index.html')