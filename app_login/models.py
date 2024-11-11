from django.db import models
from datetime import datetime

class Login(models.Model):

    id = models.AutoField(primary_key=True)

    user = models.TextField(max_length=255)

    password = models.TextField(max_length=255)

    random_hash = models.TextField(max_length=255)


class User(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.TextField(max_length=255)

    email = models.TextField(max_length=255)

    login_id = models.IntegerField()
