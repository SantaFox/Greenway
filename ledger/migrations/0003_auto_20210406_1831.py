# Generated by Django 3.1.7 on 2021-04-06 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_tag_slug'),
        ('ledger', '0002_orderpositions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderPositions',
            new_name='OrderPosition',
        ),
    ]
