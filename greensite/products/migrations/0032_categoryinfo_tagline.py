# Generated by Django 3.2 on 2021-04-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_rename_tagline_categoryinfo_shortdesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryinfo',
            name='Tagline',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
