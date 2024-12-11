from django.shortcuts import render, redirect
from django.http import JsonResponse
from app_stock.models.model_product import Product
from app_stock.models.model_history import History
from app_stock.models.model_supplier import Supplier
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *
from app_stock.util.StockUtil import *
from datetime import date
from datetime import datetime

def movement_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    movements = {
        'movements': History.objects.all()
    }

    return render(request, 'movements/index.html', movements)

def movement_entry(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    classification = ClassificationTransfer.ENTRADA

    if request.method == 'POST':
        STOCK_ENTRADA_ID = 1
        form = {}
        form['invoice'] = request.POST.get('invoice')
        form['invoice_date'] = request.POST.get('invoice_date')
        form['quantity'] = request.POST.get('quantity')
        form['supplier'] = request.POST.get('supplier')
        form['product_id'] = request.POST.get('product_id')
        form['product_name'] = request.POST.get('product_name')

        print_form(form)        

        message.messages = validate_movement(form)
        
        if message.messages:
            return render(request, 'movements/entry.html', {'messages' : message.messages, 'movement' : form, 'suppliers' : suppliers,
                                                            'classification' : classification})
        
        movement_history = History()
        movement_history.invoice = form['invoice']
        movement_history.invoice_date = form['invoice_date']
        movement_history.product_id = int(form['product_id'])
        movement_history.quantity = int(form['quantity'])
        movement_history.supplier_id = int(form['supplier'])
        movement_history.classification = classification
        movement_history.stock_id = STOCK_ENTRADA_ID
        movement_history.user_id = int(request.session['user_id'])
        movement_history.save()

        success_message = "Produto(s) cadastrado com sucesso no Estoque de Entrada."
        return render(request, 'movements/entry.html', {'success_message' : success_message})


    return render(request, 'movements/entry.html', {'suppliers' : suppliers, 'classification' : classification})

def validate_movement(movement):
    message = MessageAlert()
    if not movement['invoice'] or not movement['invoice_date'] or not movement['product_id'] or not movement['supplier'] or not movement['quantity']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    if movement['product_id'] == '':
        movement['product_id'] = 0
    if int(movement['product_id']) <= 0:
        error_text = "Selecione um Produto"
        message.add(error_text)

    if int(movement['supplier']) <= 0:
        error_text = "Selecione um Fornecedor"
        message.add(error_text)

    if movement['quantity'] == '':
        movement['quantity'] = 0
    if int(movement['quantity']) <= 0:
        error_text = "Informe uma Quantidade válida"
        message.add(error_text) 

    if movement['invoice_date']:
        if not invoice_date_is_valid(movement['invoice_date']):
            error_text = "Informe uma Data da Nota válida"
            message.add(error_text) 

    return message.messages

def invoice_date_is_valid(invoice_date):
    is_valid = True
    
    index = invoice_date.index("-")
    if index > 4:
        return False

    invoice_date_format = datetime.strptime(invoice_date, '%Y-%m-%d').date()
    today = date.today()
    if invoice_date_format > today:
        print('Data da Nota não pode ser maior que data Atual')
        return False
    

    invoice_year = invoice_date_format.year
    invoice_month = invoice_date_format.month
    invoice_day = invoice_date_format.day
    DECEMBER = 12
    JANUARY = 1

    if invoice_year - today.year == -1:
        if invoice_month == DECEMBER and today.month == JANUARY:
            if invoice_day > 27 and today.day < 4:
                return True
            else:
                return False
        else:
            return False
    
    return True

def print_form(form):
    print(form['invoice'])
    print(form['invoice_date'])
    print(form['quantity'])
    print(form['supplier'])
    print(form['product_id'])
    print(form['product_name'])

def search_product(request):
    if request.method == 'POST':
        searched = request.POST.get('searched')
        print(searched)
        products = Product.objects.filter(name__contains=searched)
        dict_products = {}
        for product in products:
            dict_products[product.id] = product.name
        print(dict_products)

    return JsonResponse(dict_products, safe=False)
