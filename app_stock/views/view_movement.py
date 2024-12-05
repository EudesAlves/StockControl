from django.shortcuts import render, redirect
from app_stock.models.model_product import Product
from app_stock.models.model_history import History
from app_stock.models.model_supplier import Supplier
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *
from app_stock.util.StockUtil import *

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
        form['product'] = request.POST.get('product')
        form['quantity'] = request.POST.get('quantity')
        form['supplier'] = request.POST.get('supplier')

        print(form['invoice'])
        print(form['invoice_date'])
        print(form['product'])
        print(form['quantity'])
        print(form['supplier'])

        
        movement_history = History()
        movement_history.invoice = form['invoice']
        movement_history.invoice_date = form['invoice_date']
        movement_history.product_id = form['product']
        movement_history.quantity = form['quantity']
        movement_history.supplier_id = form['supplier']
        movement_history.classification = classification
        movement_history.stock_id = STOCK_ENTRADA_ID
        movement_history.user_id = request.session['user_id']
        movement_history.technician_id = 1
        movement_history.save()


    return render(request, 'movements/entry.html', {'suppliers' : suppliers, 'products' : products, 'classification' : classification})