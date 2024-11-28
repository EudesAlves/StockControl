from django.shortcuts import render, redirect
from app_stock.models.model_technician import Technician
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *

def tech_list(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    techs = {
        'techs': Technician.objects.all()
    }

    return render(request, 'techs/index.html', techs)

def tech_register(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    message = MessageAlert()
    if request.method == 'POST':
        form = {}
        form['name'] = request.POST.get('tech_name')

        message.messages = validate_tech(form)
        if message.messages:
            return render(request, 'techs/register.html', {'messages' : message.messages, 'tech' : form})
        
        tech = Technician()
        tech.name = form['name']
        tech.save()

        success_message = "Técnico " +form['name']+ " cadastrado com sucesso."
        return render(request, 'techs/register.html', {'success_message' : success_message})

    return render(request, 'techs/register.html')

def tech_update(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        tech = Technician.objects.get(id=id)
        return render(request, "techs/update.html", {"tech": tech})
    
    if request.method == 'POST':
        form = {}
        form['id'] = id
        form['name'] = request.POST.get('tech_name')

        message = MessageAlert()
        message.messages = validate_tech(form)
        if message.messages:
            return render(request, 'techs/update.html', {'messages' : message.messages, 'tech' : form})

        tech = Technician.objects.get(id=id)
        tech.name = form['name']
        tech.save()

        success_message = "Técnico " +form['name']+ " atualizado com sucesso."
        return render(request, 'techs/update.html', {'success_message' : success_message, 'tech' : form})
    
def tech_delete(request, id):
    if not LoginUtil.is_logged(request):
        return redirect('login')

    if request.method == 'GET':
        tech = Technician.objects.get(id=id)
        return render(request, "techs/delete.html", {"tech": tech})
    
    if request.method == 'POST':
        form = {}
        if id:
            tech = Technician.objects.get(id=id)
            form['id'] = tech.id
            form['name'] = tech.name

            tech.delete()

        success_message = "Técnico " +form['name']+ " excluído com sucesso."
        return render(request, 'techs/delete.html', {'success_message' : success_message, 'tech' : form})

def validate_tech(tech):
    message = MessageAlert()
    if not tech['name']:
        error_text = "Todos os campos devem ser preenchidos"
        message.add(error_text)

    return message.messages