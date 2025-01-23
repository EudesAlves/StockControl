from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.db import connection
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

    populate_initial_data(request)
    
    classifications = [ ClassificationTransfer.ENTRADA, ClassificationTransfer.TRANSFERENCIA, ClassificationTransfer.RETORNO_DEFEITO ]

    stocks = Stock.objects.filter(active=True)

    stock_id = 0
    classification = ''
    list_movements = []
    dict_movements = {}

    if request.method == 'POST':
        form = {}
        stock_id = int(request.POST.get('stock'))
        classification = request.POST.get('classification')
        print(stock_id)
        print(classification)


    with connection.cursor() as cursor:
        query = """SELECT h.id, h.invoice, h.invoice_date, st.name, p.name, h.quantity, sp.name, h.classification
                FROM app_stock_history h INNER JOIN app_stock_stock st ON h.stock_id = st.id
                INNER JOIN app_stock_product p ON h.product_id = p.id
                LEFT JOIN app_stock_supplier sp ON h.supplier_id = sp.id
                WHERE h.product_id = p.id"""
        if classification != '':
            query += " AND h.classification = '"+ classification +"'"
        if stock_id > 0:
            query += " AND h.stock_id = "+ str(stock_id)
        
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                dict_movements['id'] = row[0]
                dict_movements['invoice'] = row[1]
                dict_movements['invoice_date'] = row[2]
                dict_movements['stock'] = row[3]
                dict_movements['product'] = row[4]
                dict_movements['quantity'] = row[5]
                dict_movements['supplier'] = row[6]
                dict_movements['classification'] = row[7]
                list_movements.append(dict_movements)
                dict_movements = {}

    return render(request, 'movements/index.html', { 'movements' : list_movements, 'stocks' : stocks, 'classifications' : classifications })

def movement_entry(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
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
        products = Product.objects.filter(name__contains=searched, active=True)
        dict_products = {}
        for product in products:
            dict_products[product.id] = product.name
        print(dict_products)

    return JsonResponse(dict_products, safe=False)

def movement_transference(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    stocks_origin = Stock.objects.filter(active=True)
    stocks_destination = Stock.objects.filter(active=True).exclude(id=1).values()
    classification = ClassificationTransfer.TRANSFERENCIA

    if request.method == 'POST':
        STOCK_ENTRADA_ID = 1
        form = {}
        form['stock-origin'] = request.POST.get('stock-origin')
        form['stock-destination'] = request.POST.get('stock-destination')
        form['quantity'] = request.POST.get('quantity')
        form['product_id'] = request.POST.get('product_id')
        form['product_name'] = request.POST.get('product_name')
        form['choosed_product_quantity'] = request.POST.get('choosed_product_quantity')

        message.messages = validate_transference(form)
        
        if message.messages:
            return render(request, 'movements/transference.html', {'messages' : message.messages, 'movement' : form, 'stocks_origin' : stocks_origin,
                                                            'stocks_destination' : stocks_destination, 'classification' : classification})
        
        transfer_origin = History()
        transfer_origin.product_id = int(form['product_id'])
        transfer_origin.quantity = (-1)*int(form['quantity'])
        transfer_origin.classification = classification
        transfer_origin.stock_id = form['stock-origin']
        transfer_origin.user_id = int(request.session['user_id'])
        transfer_origin.save()

        transfer_destination = History()
        transfer_destination.product_id = int(form['product_id'])
        transfer_destination.quantity = int(form['quantity'])
        transfer_destination.classification = classification
        transfer_destination.stock_id = form['stock-destination']
        transfer_destination.user_id = int(request.session['user_id'])
        transfer_destination.save()

        success_message = "Transferência realizada com sucesso."
        return render(request, 'movements/transference.html', {'success_message' : success_message, 'stocks_origin' : stocks_origin, 'stocks_destination' : stocks_destination})


    return render(request, 'movements/transference.html', {'stocks_origin' : stocks_origin, 'stocks_destination' : stocks_destination,
                                                     'classification' : classification})

def validate_transference(movement):
    message = MessageAlert()
    if not movement['stock-origin'] or not movement['stock-destination'] or not movement['product_id'] or not movement['quantity'] or not movement['choosed_product_quantity']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    if movement['product_id'] == '':
        movement['product_id'] = 0
    if int(movement['product_id']) <= 0:
        error_text = "Selecione um Produto"
        message.add(error_text)

    if int(movement['stock-origin']) <= 0:
        error_text = "Selecione o Estoque de Origem"
        message.add(error_text)

    if int(movement['stock-destination']) <= 0:
        error_text = "Selecione o Estoque de Destino"
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

def search_product_quantity(request):
    searched = ''
    if request.method == 'POST':
        searched = request.POST.get('searched')
        stock_id = request.POST.get('stock_id')

    list_products = []
    dict_products = {}
    with connection.cursor() as cursor:
        query = """SELECT p.id, p.name, SUM(h.quantity) FROM app_stock_product p INNER JOIN app_stock_history h ON p.id = h.product_id
                WHERE p.name LIKE '%"""+ searched +"%' AND p.active = 1 AND h.stock_id = "+ str(stock_id) +""
        query += " GROUP BY p.id"        
        
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                dict_products['id'] = row[0]
                dict_products['name'] = row[1]
                dict_products['quantity'] = row[2]
                list_products.append(dict_products)
                dict_products = {}

    print('dict_produtos: ')
    for item in dict_products:
        print(item[0])
        print(item[1])

    data = json.dumps(list_products)
    return JsonResponse(data, safe=False)

def populate_initial_data(request):
    if not 'initial_stock' in request.session:
        request.session['initial_stock'] = 1
        StockUtil.populate_initial_stock()