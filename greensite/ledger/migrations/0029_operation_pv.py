# Generated by Django 3.2 on 2021-04-24 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0028_counterparty_check_counterparty_supplier_or_customer_is_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='PV',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
