# Generated by Django 3.1.7 on 2021-04-02 21:06

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20210402_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tab',
            name='Text',
            field=martor.models.MartorField(blank=True),
        ),
    ]