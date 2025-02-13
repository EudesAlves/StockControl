from django.shortcuts import render, redirect
from app_stock.models.model_stock import Stock
from app_stock.models.model_history import History
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *


def stock_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    stocks = {
        'stocks': Stock.objects.filter(active=True)
    }

    return render(request, 'stocks/index.html', stocks)

def stock_register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    for_use_checked = False
    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('stock_name')
        form['for_use'] = False
        checkbox_for_use = request.POST.get('stock_for_use')
        if checkbox_for_use == 'on':
            form['for_use'] = True
            for_use_checked = True
        
        print(form['for_use'])
        

        message.messages = validate_stock(form)
        if message.messages:
            return render(request, 'stocks/register.html', {'messages' : message.messages, 'stock' : form, 'for_use_checked' : for_use_checked})
        
        stock = Stock()
        stock.name = form['name']
        stock.for_use = bool(form['for_use'])
        stock.save()

        success_message = "Estoque " +form['name']+ " cadastrado com sucesso."
        return render(request, 'stocks/register.html', {'success_message' : success_message})

    return render(request, 'stocks/register.html', {'for_use_checked' : for_use_checked})

def stock_update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    for_use_checked = False
    if request.method == 'GET':
        stock = Stock.objects.get(id=id)
        if stock.for_use:
            for_use_checked = True

        return render(request, 'stocks/update.html', {'stock': stock, 'for_use_checked': for_use_checked})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('stock_name')
        form['for_use'] = False
        checkbox_for_use = request.POST.get('stock_for_use')
        if checkbox_for_use == 'on':
            form['for_use'] = True
            for_use_checked = True

        message = MessageAlert()
        message.messages = validate_stock(form)
        if message.messages:
            return render(request, 'stocks/update.html', {'messages' : message.messages, 'stock' : form, 'for_use_checked' : for_use_checked})

        stock = Stock.objects.get(id=id)
        stock.name = form['name']
        stock.for_use = bool(form['for_use'])
        stock.save()

        success_message = "Estoque " +form['name']+ " atualizado com sucesso."
        return render(request, 'stocks/update.html', {'success_message' : success_message, 'stock' : form, 'for_use_checked' : for_use_checked})

def stock_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    stock = Stock.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "stocks/delete.html", {"stock": stock})
    
    if request.method == 'POST':
        form = {}
        if id:
            stock = Stock.objects.get(id=id)
            form['id'] = stock.id
            form['name'] = stock.name

            stock.active = False
            stock.save()

        success_message = "Estoque " +form['name']+ " excluído com sucesso."
        return render(request, 'stocks/delete.html', {'success_message' : success_message, 'stock' : form})

def validate_stock(stock):
    message = MessageAlert()
    if not stock['name']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    return message.messages
