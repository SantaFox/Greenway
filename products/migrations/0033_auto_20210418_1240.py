# Generated by Django 3.2 on 2021-04-18 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_categoryinfo_tagline'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryinfo',
            name='LongDesc',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='categoryinfo',
            name='ShortDesc',
            field=models.CharField(max_length=100),
        ),
    ]
