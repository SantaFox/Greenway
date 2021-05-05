# Generated by Django 3.2 on 2021-04-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0048_alter_customerorder_courierservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierorder',
            name='CourierService',
            field=models.CharField(blank=True, choices=[('DHL', 'DHL Express'), ('CZP', 'Czech Post'), ('POST', 'Ordinary Post')], max_length=10, null=True),
        ),
    ]