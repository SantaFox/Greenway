# Generated by Django 3.1.7 on 2021-04-07 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0014_remove_orderposition_order'),
    ]

    operations = [
        migrations.RenameModel('OrderPosition', 'OperationPosition')
    ]
