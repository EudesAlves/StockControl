# Generated by Django 5.1.3 on 2024-12-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_stock', '0004_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='invoice',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='invoice_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='supplier_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='technician_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
