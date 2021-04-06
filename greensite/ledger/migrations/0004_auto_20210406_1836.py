# Generated by Django 3.1.7 on 2021-04-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0003_auto_20210406_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='Name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='account',
            constraint=models.UniqueConstraint(fields=('User', 'Name'), name='unique_Account'),
        ),
    ]