# Generated by Django 5.1.3 on 2025-01-03 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_login', '0003_rename_user_login_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='active',
            field=models.BooleanField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=1),
        ),
    ]
