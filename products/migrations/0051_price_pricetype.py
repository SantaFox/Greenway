# Generated by Django 4.1.1 on 2022-10-31 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0050_alter_action_dateend'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='PriceType',
            field=models.CharField(choices=[('C', 'Customer'), ('S', 'Supplier')], default='S', max_length=1),
            preserve_default=False,
        ),
    ]
