# Generated by Django 3.2 on 2021-05-04 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0039_price_gft'),
        ('ledger', '0053_auto_20210502_2332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='Type',
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='Currency',
            field=models.ForeignKey(help_text='Currency of the sell price', on_delete=django.db.models.deletion.PROTECT, to='products.currency', verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='Discount',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Discount applied to total amount for the position', max_digits=10, null=True, verbose_name='Discount'),
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='DiscountReason',
            field=models.CharField(blank=True, help_text='Reason for provision of Discount', max_length=50, verbose_name='Discount Reason'),
        ),
        migrations.AlterField(
            model_name='customerorderposition',
            name='Price',
            field=models.DecimalField(decimal_places=2, help_text='Sell price per one Product', max_digits=10, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='operationposition',
            name='Product',
            field=models.ForeignKey(help_text='Product', on_delete=django.db.models.deletion.PROTECT, to='products.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='operationposition',
            name='Quantity',
            field=models.PositiveIntegerField(help_text='Quantity of Products', verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='supplierorderposition',
            name='Currency',
            field=models.ForeignKey(blank=True, help_text='Currency of the paid price', null=True, on_delete=django.db.models.deletion.PROTECT, to='products.currency', verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='supplierorderposition',
            name='Price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Paid price per one Product', max_digits=10, null=True, verbose_name='Price'),
        ),
    ]