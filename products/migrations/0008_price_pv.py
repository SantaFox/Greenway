# Generated by Django 3.1.7 on 2021-03-30 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210331_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='PV',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
