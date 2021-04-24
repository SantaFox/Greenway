# Generated by Django 3.2 on 2021-04-23 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0027_auto_20210423_0925'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='counterparty',
            constraint=models.CheckConstraint(check=models.Q(('IsSupplier', True), ('IsCustomer', True), _connector='OR'), name='check_Counterparty_Supplier_or_Customer_is_Set'),
        ),
    ]
