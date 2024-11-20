from django.db import models
from datetime import datetime
from django.utils import timezone

class Login(models.Model):

    id = models.AutoField(primary_key=True)

    email = models.TextField(max_length=255)

    password = models.TextField(max_length=255)

    random_hash = models.TextField(max_length=255)

    creation_date = models.DateTimeField(auto_now_add=True)


class User(models.Model):

    id = models.AutoField(primary_key=True)

    name = models.TextField(max_length=255)

    email = models.TextField(max_length=255)

    login_id = models.IntegerField()

    creation_date = models.DateTimeField(auto_now_add=True)
