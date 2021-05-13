# Generated by Django 3.2.2 on 2021-05-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_auto_20210513_1330'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='carousel',
            name='unique_Carousel',
        ),
        migrations.RemoveConstraint(
            model_name='featurette',
            name='unique_Featurette',
        ),
        migrations.AddField(
            model_name='carousel',
            name='Order',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featurette',
            name='Order',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='carousel',
            constraint=models.UniqueConstraint(fields=('Order',), name='unique_Carousel'),
        ),
    ]
