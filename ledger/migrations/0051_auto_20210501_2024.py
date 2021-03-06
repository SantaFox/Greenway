# Generated by Django 3.2 on 2021-05-01 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0050_auto_20210501_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='Counterparty',
            field=models.ForeignKey(blank=True, help_text='Registered Customer', null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.counterparty', verbose_name='Customer Name'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='CourierService',
            field=models.CharField(blank=True, choices=[('DHL', 'DHL Express'), ('CZP', 'Czech Post'), ('POST', 'Ordinary Post')], help_text='Select one from provided Courier Services', max_length=10, null=True, verbose_name='Courier Service Name'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='DateDispatched',
            field=models.DateField(blank=True, help_text='Date when this Order was dispatched to the Customer. Until then, the Order is prepared but held in Storage.', null=True, verbose_name='Dispatch Date'),
        ),
    ]
