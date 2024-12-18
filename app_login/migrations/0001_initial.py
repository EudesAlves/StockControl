# Generated by Django 5.1.3 on 2024-11-11 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.TextField(max_length=255)),
                ('password', models.TextField(max_length=255)),
                ('random_hash', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('email', models.TextField(max_length=255)),
                ('login_id', models.IntegerField()),
            ],
        ),
    ]
