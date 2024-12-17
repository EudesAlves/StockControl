from django.db import models
from django.utils.translation import gettext_lazy as _
from app_stock.models.model_stock import Stock
from app_login.models import Login
from app_login.models import User
from app_login.util.LoginUtil import *

class ClassificationTransfer(models.TextChoices):
    ENTRADA = 'Entrada', _('Entrada')
    TRANSFERENCIA = 'Transferência', _('Transferência')
    RETORNO_DEFEITO = 'Retorno Defeito', _('Retorno Defeito')

class StockUtil():
    def populate_initial_data():
        populate_initial_stock()

    def populate_initial_stock():
        stocks = Stock.objects.all()
        if stocks.count() == 0:
            stock = Stock()
            stock.name = ClassificationTransfer.ENTRADA
            stock.save()
