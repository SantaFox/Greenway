# Generated by Django 3.2.9 on 2021-12-09 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0043_auto_20211209_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='Comment',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
