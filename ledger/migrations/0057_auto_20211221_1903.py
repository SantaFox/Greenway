# Generated by Django 3.2.9 on 2021-12-21 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0056_auto_20211221_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationposition',
            name='TransactionType',
        ),
        migrations.AddField(
            model_name='itemsetbreakdownposition',
            name='TransactionType',
            field=models.CharField(choices=[('D', 'Debit'), ('C', 'Credit')], default='D', max_length=1),
            preserve_default=False,
        ),
    ]