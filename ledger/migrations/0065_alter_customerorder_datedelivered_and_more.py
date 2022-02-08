# Generated by Django 4.0.2 on 2022-02-04 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0064_auto_20220114_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerorder',
            name='DateDelivered',
            field=models.DateField(blank=True, help_text='Date when this Order was delivered to the Customer. In case of Detailed Delivery, the date of last delivery is used', null=True, verbose_name='Delivery Date'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='DateDispatched',
            field=models.DateField(blank=True, help_text='Date when this Order was dispatched to the Customer. Until then, the Order is prepared but held in Storage', null=True, verbose_name='Dispatch Date'),
        ),
        migrations.AlterField(
            model_name='customerorder',
            name='DeliveryPrice',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Price of delivery in the same currency as Amount, if Customer is charged for it. Included in total Amount.', max_digits=10, null=True, verbose_name='Delivery price'),
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='DateDelivered',
            field=models.DateField(blank=True, help_text='Date when this Order position was delivered to the Customer. This field is available only if Detailed Deliver set in Order.', null=True, verbose_name='Delivery Date'),
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='Status',
            field=models.IntegerField(blank=True, choices=[(1, 'In stock / prepared for delivery'), (2, 'In stock / should be ordered'), (3, 'Not in stock / need to be ordered'), (4, 'Not in stock / waiting for incoming'), (5, 'Not in stock / no delivery control'), (6, 'Delivered to customer')], help_text='Ordering status of this position', null=True, verbose_name='Ordering status'),
        ),
        migrations.AlterField(
            model_name='supplierorder',
            name='DeliveryPrice',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Price of delivery in the same currency as Amount, if separately provided by the Supplier. Included in total Amount.', max_digits=10, null=True, verbose_name='Delivery price'),
        ),
    ]