# Generated by Django 3.1.7 on 2021-04-06 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0006_auto_20210406_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='DateDelivered',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='DateDispatched',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='DatePlaced',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='TrackingNumber',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
