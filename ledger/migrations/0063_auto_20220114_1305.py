# Generated by Django 3.2.9 on 2022-01-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0062_auto_20220113_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparty',
            name='IsCustomer',
            field=models.BooleanField(default=False, help_text='Act as Customer', verbose_name='Is Customer?'),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='IsSupplier',
            field=models.BooleanField(default=False, help_text='Act as Supplier', verbose_name='Is Supplier?'),
        ),
    ]
