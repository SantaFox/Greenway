# Generated by Django 3.2 on 2021-04-07 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0018_operationatom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atomproductoperation',
            name='Operation',
        ),
        migrations.DeleteModel(
            name='AtomCashOperation',
        ),
        migrations.DeleteModel(
            name='AtomProductOperation',
        ),
    ]
