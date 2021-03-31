# Generated by Django 3.1.7 on 2021-03-30 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='Symbol',
            field=models.CharField(blank=True, max_length=1),
        ),
        migrations.AddField(
            model_name='language',
            name='Name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]