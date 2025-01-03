from django.db import models

class Technician(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.TextField(max_length=255)

    creation_date = models.DateTimeField(auto_now_add=True)