from django.shortcuts import render, redirect
from app_stock.models.model_product import Product
from app_stock.models.model_history import History
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *

def movement_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    movements = {
        'movements': History.objects.all()
    }

    return render(request, 'movements/index.html', movements)

def movement_entry(request):
    return render(request, 'movements/index.html')