# Generated by Django 3.2.2 on 2021-05-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0006_auto_20210517_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='HeaderClass',
            field=models.CharField(blank=True, help_text='Bootstrap class for header over image. May be used for color change.', max_length=255, verbose_name='Header Class'),
        ),
    ]