# Generated by Django 3.2 on 2021-04-26 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0040_supplierorder_greenwayorderid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplierorder',
            old_name='GreenwayOrderId',
            new_name='GreenwayOrderNum',
        ),
    ]
