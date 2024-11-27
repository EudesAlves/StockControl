from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.TextField(max_length=255)

    invoice = models.TextField(max_length=255)

    invoice_date = models.DateField()

    creation_date = models.DateTimeField(auto_now_add=True)