# Generated by Django 3.1.7 on 2021-04-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_language_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='Flag',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='language',
            name='Name',
            field=models.CharField(max_length=50),
        ),
    ]