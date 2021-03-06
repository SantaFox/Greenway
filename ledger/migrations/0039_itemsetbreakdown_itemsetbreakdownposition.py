# Generated by Django 3.2 on 2021-04-25 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20210419_1208'),
        ('ledger', '0038_customerorder_detaileddelivery'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemSetBreakdownPosition',
            fields=[
                ('operationposition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ledger.operationposition')),
            ],
            options={
                'verbose_name_plural': 'Item Set Breakdown Positions',
            },
            bases=('ledger.operationposition',),
        ),
        migrations.CreateModel(
            name='ItemSetBreakdown',
            fields=[
                ('operation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ledger.operation')),
                ('Quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('Product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Item Set Breakdowns',
            },
            bases=('ledger.operation',),
        ),
    ]
