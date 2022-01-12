# Generated by Django 3.2.9 on 2022-01-11 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0050_alter_action_dateend'),
        ('ledger', '0060_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='CreditAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='credit_account', to='ledger.account'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='CreditAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='CreditCurrency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='credit_currency', to='products.currency'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='DebitAccount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='debit_account', to='ledger.account'),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='DebitAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='DebitCurrency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='debit_currency', to='products.currency'),
        ),
    ]