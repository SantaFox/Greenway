# Generated by Django 3.2 on 2021-04-25 15:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20210419_1208'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledger', '0033_auto_20210425_1812'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OperSupplierOrder',
            new_name='SupplierOrder',
        ),
    ]
