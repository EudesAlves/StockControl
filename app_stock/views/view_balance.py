from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.db.models import Sum
from django.db import connection
from app_login.util import LoginUtil
from app_login.util import MessageAlert
from app_login.util.LoginUtil import *
from app_login.util.MessageAlert import *
from app_stock.util.StockUtil import *
from datetime import date
from datetime import datetime

def balance(request):
    if not LoginUtil.is_logged(request):
        return redirect('login')
    
    list_products = []
    dict_products = {}
    total_balance = []

    stocks = Stock.objects.filter(active=True)
    searched = ''
    if request.method == 'POST':
        searched = request.POST.get('product_name')

    with connection.cursor() as cursor:
        query = """SELECT DISTINCT p.id, p.name FROM app_stock_product p
                INNER JOIN app_stock_history h ON h.product_id = p.id
                WHERE p.active = 1 AND p.name LIKE '%"""+ searched +"%'"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                dict_products['id'] = row[0]
                dict_products['name'] = row[1]
                list_products.append(dict_products)
                dict_products = {}

        
        for product in list_products:
            quantity_of_products = []
            total_quantity = 0

            for stock in stocks:
                query = """SELECT SUM(h.quantity) FROM app_stock_product p 
                        INNER JOIN app_stock_history h ON p.id = h.product_id
                        WHERE p.active = 1 AND h.stock_id = """+ str(stock.id) +" AND p.id = " + str(product['id'])
                query += " GROUP BY p.id"
            
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if rows:
                    for row in rows:
                        quantity_of_products.append(str(row[0]))
                else:
                    quantity_of_products.append(str(0))
                total_quantity += int(quantity_of_products[len(quantity_of_products)-1])
            
            total_balance.append({
                'name': product['name'],
                'quantities': quantity_of_products,
                'total': total_quantity
            })


    return render(request, 'movements/balance.html', { 'products': list_products, 'stocks': stocks, 'total_balance': total_balance, 'product_name': searched })