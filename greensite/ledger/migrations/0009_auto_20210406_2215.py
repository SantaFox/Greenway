# Generated by Django 3.1.7 on 2021-04-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0008_auto_20210406_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='DateCreated',
            field=models.DateField(),
        ),
    ]
