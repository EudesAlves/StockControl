from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.TextField(max_length=255)

    for_use = models.BooleanField(default=0)

    active = models.BooleanField(default=1)

    creation_date = models.DateTimeField(auto_now_add=True)