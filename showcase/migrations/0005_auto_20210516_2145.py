# Generated by Django 3.2.2 on 2021-05-16 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0004_auto_20210513_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurette',
            name='ButtonAction',
            field=models.CharField(blank=True, help_text='Action fired when carousel button is pressed. If empty, no button is shown.', max_length=255, verbose_name='Button Action'),
        ),
        migrations.AddField(
            model_name='featuretteinfo',
            name='ButtonText',
            field=models.CharField(blank=True, help_text='Text shown on the ', max_length=50, verbose_name='Button Text'),
        ),
    ]
