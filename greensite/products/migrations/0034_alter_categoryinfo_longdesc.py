# Generated by Django 3.2 on 2021-04-18 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0033_auto_20210418_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryinfo',
            name='LongDesc',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
