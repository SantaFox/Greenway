# Generated by Django 3.2 on 2021-04-30 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0038_price_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='GFT',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
