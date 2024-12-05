from django.db import models

class History(models.Model):
    id = models.AutoField(primary_key=True)

    invoice = models.TextField(max_length=100, blank=True)

    invoice_date = models.DateTimeField(blank=True)
    
    stock_id = models.IntegerField()

    product_id = models.IntegerField()

    quantity = models.IntegerField()

    supplier_id = models.IntegerField(blank=True)

    technician_id = models.IntegerField(blank=True, null=True)

    classification = models.TextField(max_length=100)

    user_id = models.IntegerField()

    creation_date = models.DateTimeField(auto_now_add=True)