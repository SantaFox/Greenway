# Generated by Django 3.2 on 2021-04-25 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0037_auto_20210419_1208'),
        ('ledger', '0036_auto_20210425_2110'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerOrderPosition',
            fields=[
                ('operationposition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ledger.operationposition')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('DiscountReason', models.CharField(blank=True, max_length=50)),
                ('CustomerOrderStatus', models.IntegerField(blank=True, choices=[(1, 'In stock / prepared for delivery'), (2, 'In stock / should be ordered'), (3, 'Not in stock / need to be ordered'), (4, 'Not in stock / waiting for incoming'), (5, 'Not in stock / no delivery control'), (6, 'Delivered to customer')], null=True)),
                ('DateDelivered', models.DateField(blank=True, null=True)),
                ('Currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.currency')),
            ],
            options={
                'verbose_name_plural': 'Customer Order Positions',
            },
            bases=('ledger.operationposition',),
        ),
    ]
