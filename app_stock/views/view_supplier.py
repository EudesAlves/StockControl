from django.shortcuts import render, redirect
from app_stock.models.model_supplier import Supplier
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *

def supplier_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    suppliers = {
        'suppliers': Supplier.objects.all()
    }

    return render(request, 'suppliers/index.html', suppliers)

def supplier_register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('supplier_name')

        message.messages = validate_supplier(form)
        if message.messages:
            return render(request, 'suppliers/register.html', {'messages' : message.messages, 'supplier' : form})
        
        supplier = Supplier()
        supplier.name = form['name']
        supplier.save()

        success_message = "Fornecedor " +form['name']+ " cadastrado com sucesso."
        return render(request, 'suppliers/register.html', {'success_message' : success_message})

    return render(request, 'suppliers/register.html')

def supplier_update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        supplier = Supplier.objects.get(id=id)
        return render(request, "suppliers/update.html", {"supplier": supplier})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('supplier_name')

        message = MessageAlert()
        message.messages = validate_supplier(form)
        if message.messages:
            return render(request, 'suppliers/update.html', {'messages' : message.messages, 'supplier' : form})

        supplier = Supplier.objects.get(id=id)
        supplier.name = form['name']
        supplier.save()

        success_message = "Fornecedor " +form['name']+ " atualizado com sucesso."
        return render(request, 'suppliers/update.html', {'success_message' : success_message, 'supplier' : form})
    
def supplier_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        supplier = Supplier.objects.get(id=id)
        return render(request, "suppliers/delete.html", {"supplier": supplier})
    
    if request.method == 'POST':
        form = {}
        if id:
            supplier = Supplier.objects.get(id=id)
            form['id'] = supplier.id
            form['name'] = supplier.name

            supplier.delete()

        success_message = "Fornecedor " +form['name']+ " excluído com sucesso."
        return render(request, 'suppliers/delete.html', {'success_message' : success_message, 'supplier' : form})

def validate_supplier(supplier):
    message = MessageAlert()
    if not supplier['name']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    return message.messages