# Generated by Django 3.2.2 on 2021-05-17 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0005_auto_20210516_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='ButtonAction',
            field=models.CharField(blank=True, help_text='Action fired when carousel button is pressed. If empty, no button is shown.', max_length=255, verbose_name='Button Action'),
        ),
        migrations.AddField(
            model_name='carousel',
            name='TextClass',
            field=models.CharField(blank=True, help_text='Bootstrap class for text over image. May be used for color change.', max_length=255, verbose_name='Text Class'),
        ),
        migrations.AddField(
            model_name='carouselinfo',
            name='ButtonText',
            field=models.CharField(blank=True, help_text='Text shown on the carousel text block', max_length=50, verbose_name='Button Text'),
        ),
        migrations.AlterField(
            model_name='featurette',
            name='ButtonAction',
            field=models.CharField(blank=True, help_text='Action fired when featurette button is pressed. If empty, no button is shown.', max_length=255, verbose_name='Button Action'),
        ),
    ]