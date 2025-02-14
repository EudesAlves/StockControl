from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.db import connection
from app_stock.models.model_product import Product
from app_stock.models.model_history import History
from app_stock.models.model_supplier import Supplier
from app_stock.models.model_technician import Technician
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *
from app_stock.util.StockUtil import *
from datetime import date
from datetime import datetime


def withdraw_return(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')
    
    message = MessageAlert()
    stock = Stock.objects.filter(active=True, for_use=True)
    
    technicians = Technician.objects.filter(active=True)
    classifications = [ ClassificationTransfer.RETIRADA, ClassificationTransfer.DEVOLUCAO ]
    stock = stock.first()

    if request.method == 'POST':
        form = {}
        form['classification'] = request.POST.get('classification')
        form['stock_id'] = request.POST.get('stock_id')
        form['technician_id'] = request.POST.get('technician')
        form['quantity'] = request.POST.get('quantity')
        form['product_id'] = request.POST.get('product_id')
        form['product_name'] = request.POST.get('product_name')
        form['choosed_product_quantity'] = request.POST.get('choosed_product_quantity')

        message.messages = validate_movement(form)

        if message.messages:
            return render(request, 'movements/withdraw.html', {'messages' : message.messages, 'movement' : form, 'stock' : stock,
                                                               'technicians' : technicians, 'classifications' : classifications})
        
        if form['classification'] == ClassificationTransfer.RETIRADA:
            form['quantity'] = int(form['quantity']) *-1

        history = History()
        history.product_id = int(form['product_id'])
        history.quantity = int(form['quantity'])
        history.classification = form['classification']
        history.stock_id = form['stock_id']
        history.technician_id = form['technician_id']
        history.user_id = int(request.session['user_id'])
        history.save()

        success_message = "Operação realizada com sucesso."
        return render(request, 'movements/withdraw.html', {'success_message' : success_message, 'stock' : stock, 'technicians' : technicians, 'classifications' : classifications})

    
    return render(request, 'movements/withdraw.html', {'stock' : stock, 'technicians' : technicians,
                                                     'classifications' : classifications})

def validate_movement(movement):
    message = MessageAlert()
    if not movement['stock_id'] or not movement['technician_id'] or not movement['product_id'] or not movement['quantity'] or not movement['choosed_product_quantity'] or not movement['classification']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    if movement['product_id'] == '':
        movement['product_id'] = 0
    if int(movement['product_id']) <= 0:
        error_text = "Selecione um Produto"
        message.add(error_text)

    if int(movement['stock_id']) <= 0:
        error_text = "Selecione o Estoque"
        message.add(error_text)

    if int(movement['technician_id']) <= 0:
        error_text = "Selecione o Técnico"
        message.add(error_text)

    if movement['quantity'] == '':
        movement['quantity'] = 0
    if int(movement['quantity']) <= 0:
        error_text = "Informe uma Quantidade válida"
        message.add(error_text)
    if movement['choosed_product_quantity'] == '':
        movement['choosed_product_quantity'] = 0 
    if int(movement['quantity']) > int(movement['choosed_product_quantity']):
        error_text = "Produto selecionado não possui Quantidade suficiente"
        message.add(error_text)

    return message.messages