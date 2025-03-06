"""
URL configuration for stock_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from app_login.views import view_login
from app_login.views import view_user
from app_stock.views import view_technician
from app_stock.views import view_product
from app_stock.views import view_supplier
from app_stock.views import view_stock
from app_stock.views import view_movement
from app_stock.views import view_withdraw
from app_stock.views import view_balance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', view_login.login, name = 'login'),
    path('login/validate_login', view_login.validate_login, name = 'validate_login'),
    path('login/logout', view_login.logout, name = 'logout'),

    path('users/', view_user.user_list, name = 'user_list'),
    path('users/register/', view_user.user_register, name = 'user_register'),
    path('users/update/<int:id>', view_user.user_update, name = 'user_update'),
    path('users/delete/<int:id>', view_user.user_delete, name = 'user_delete'),

    path('techs/', view_technician.tech_list, name = 'tech_list'),
    path('techs/register', view_technician.tech_register, name = 'tech_register'),
    path('techs/update/<int:id>', view_technician.tech_update, name = 'tech_update'),
    path('techs/delete/<int:id>', view_technician.tech_delete, name = 'tech_delete'),

    path('suppliers/', view_supplier.supplier_list, name = 'supplier_list'),
    path('suppliers/register', view_supplier.supplier_register, name = 'supplier_register'),
    path('suppliers/update/<int:id>', view_supplier.supplier_update, name = 'supplier_update'),
    path('suppliers/delete/<int:id>', view_supplier.supplier_delete, name = 'supplier_delete'),

    path('products/', view_product.product_list, name = 'product_list'),
    path('products/register', view_product.product_register, name = 'product_register'),
    path('products/update/<int:id>', view_product.product_update, name = 'product_update'),
    path('products/delete/<int:id>', view_product.product_delete, name = 'product_delete'),

    path('stocks/', view_stock.stock_list, name = 'stock_list'),
    path('stocks/register', view_stock.stock_register, name = 'stock_register'),
    path('stocks/update/<int:id>', view_stock.stock_update, name = 'stock_update'),
    path('stocks/delete/<int:id>', view_stock.stock_delete, name = 'stock_delete'),

    path('movements/', view_movement.movement_list, name = 'movement_list'),
    path('movements/entry', view_movement.movement_entry, name = 'movement_entry'),
    path('movements/search_product', view_movement.search_product, name = 'search_product'),
    path('movements/transference', view_movement.movement_transference, name = 'movement_transference'),
    path('movements/search_product_quantity', view_movement.search_product_quantity, name = 'search_product_quantity'),
    path('movements/withdraw', view_withdraw.withdraw_return, name = 'withdraw'),
    path('movements/balance', view_balance.balance, name = 'balance'),
    

    path('', lambda req: redirect('/movements/')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
