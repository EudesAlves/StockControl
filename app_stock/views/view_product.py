from django.shortcuts import render, redirect
from app_stock.models.model_product import Product
from app_stock.models.model_history import History
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *

def product_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    products = {
        'products': Product.objects.filter(active=True)
    }

    return render(request, 'products/index.html', products)

def product_register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('product_name')

        message.messages = validate_product(form)
        if message.messages:
            return render(request, 'products/register.html', {'messages' : message.messages, 'product' : form})
        
        product = Product()
        product.name = form['name']
        product.save()

        success_message = "Produto " +form['name']+ " cadastrado com sucesso."
        return render(request, 'products/register.html', {'success_message' : success_message})

    return render(request, 'products/register.html')

def product_update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        product = Product.objects.get(id=id)
        return render(request, "products/update.html", {"product": product})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('product_name')

        message = MessageAlert()
        message.messages = validate_product(form)
        if message.messages:
            return render(request, 'products/update.html', {'messages' : message.messages, 'product' : form})

        product = Product.objects.get(id=id)
        product.name = form['name']
        product.save()

        success_message = "Produto " +form['name']+ " atualizado com sucesso."
        return render(request, 'products/update.html', {'success_message' : success_message, 'product' : form})

def product_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    product = Product.objects.get(id=id)
    if request.method == 'GET':
        return render(request, "products/delete.html", {"product": product})
    
    if request.method == 'POST':
        form = {}
        if id:
            product = Product.objects.get(id=id)
            form['id'] = product.id
            form['name'] = product.name

            product.active = False
            product.save()

        success_message = "Produto " +form['name']+ " excluído com sucesso."
        return render(request, 'products/delete.html', {'success_message' : success_message, 'product' : form})

def validate_product(product):
    message = MessageAlert()
    if not product['name']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    return message.messages
