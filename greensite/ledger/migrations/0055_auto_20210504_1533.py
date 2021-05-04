# Generated by Django 3.2 on 2021-05-04 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0054_auto_20210504_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='CourierService',
            field=models.CharField(blank=True, choices=[('DHL', 'DHL Express'), ('AKIS', 'Akis Express'), ('CZP', 'Czech Post'), ('POST', 'Ordinary Post')], help_text='Select one from provided Courier Services', max_length=10, null=True, verbose_name='Courier Service Name'),
        ),
        migrations.AlterField(
            model_name='supplierorder',
            name='CourierService',
            field=models.CharField(blank=True, choices=[('DHL', 'DHL Express'), ('AKIS', 'Akis Express'), ('CZP', 'Czech Post'), ('POST', 'Ordinary Post')], max_length=10, null=True),
        ),
    ]
