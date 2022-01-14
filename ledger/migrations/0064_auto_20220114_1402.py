# Generated by Django 3.2.9 on 2022-01-14 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0063_auto_20220114_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparty',
            name='IsCustomer',
            field=models.BooleanField(default=False, help_text='Counterparty act as Customer and can be selected in Customer Order', verbose_name='Act as Customer'),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='IsSupplier',
            field=models.BooleanField(default=False, help_text='Counterparty act as Supplier and can be selected in Supplier Order', verbose_name='Act as Supplier'),
        ),
    ]