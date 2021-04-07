# Generated by Django 3.1.7 on 2021-04-07 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0012_orderposition_operation'),
    ]

    operations = [
        migrations.AddField(
            model_name='atomcashoperation',
            name='Operation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ledger.operation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='atomproductoperation',
            name='Operation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ledger.operation'),
            preserve_default=False,
        ),
    ]
