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
        'stocks': Stock.objects.all()
    }

    return render(request, 'stocks/index.html', stocks)

def stock_register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('stock_name')

        message.messages = validate_stock(form)
        if message.messages:
            return render(request, 'stocks/register.html', {'messages' : message.messages, 'stock' : form})
        
        stock = Stock()
        stock.name = form['name']
        stock.save()

        success_message = "Estoque " +form['name']+ " cadastrado com sucesso."
        return render(request, 'stocks/register.html', {'success_message' : success_message})

    return render(request, 'stocks/register.html')

def stock_update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        stock = Stock.objects.get(id=id)
        return render(request, "stocks/update.html", {"stock": stock})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('stock_name')

        message = MessageAlert()
        message.messages = validate_stock(form)
        if message.messages:
            return render(request, 'stocks/update.html', {'messages' : message.messages, 'stock' : form})

        stock = Stock.objects.get(id=id)
        stock.name = form['name']
        stock.save()

        success_message = "Estoque " +form['name']+ " atualizado com sucesso."
        return render(request, 'stocks/update.html', {'success_message' : success_message, 'stock' : form})

def stock_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    stock = Stock.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "stocks/delete.html", {"stock": stock})
    
    if request.method == 'POST':
        form = {}
        if id:
            message = MessageAlert()
            message.messages = check_dependency(id)
            if message.messages:
                return render(request, "stocks/delete.html", {'messages' : message.messages, "stock": stock})

            stock = Stock.objects.get(id=id)
            form['id'] = stock.id
            form['name'] = stock.name

            stock.delete()

        success_message = "Estoque " +form['name']+ " excluído com sucesso."
        return render(request, 'stocks/delete.html', {'success_message' : success_message, 'stock' : form})

def validate_stock(stock):
    message = MessageAlert()
    if not stock['name']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    return message.messages

def check_dependency(stock_id):
    message = MessageAlert()
    queryset = History.objects.filter(stock_id=stock_id)
    if queryset.count() > 0:
        error_text = "Este estoque está relacionado a uma Movimentação e não pode ser excluído."
        message.add(error_text)
    
    return message.messages