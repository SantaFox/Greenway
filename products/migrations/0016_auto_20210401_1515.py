# Generated by Django 3.1.7 on 2021-04-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210401_1510'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('Order',), name='unique_Group'),
        ),
    ]