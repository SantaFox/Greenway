# Generated by Django 3.2 on 2021-04-07 18:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0015_auto_20210407_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='operation',
            name='DateOperation',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
