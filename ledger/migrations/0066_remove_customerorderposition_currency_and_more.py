# Generated by Django 4.0.2 on 2022-03-29 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0065_alter_customerorder_datedelivered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerorderposition',
            name='Currency',
        ),
        migrations.AddField(
            model_name='counterparty',
            name='Coordinates',
            field=models.CharField(blank=True, help_text='Coordinates (in digital form, separated by comma) to be shown on the map', max_length=50, verbose_name='Map Coordinates'),
        ),
    ]
