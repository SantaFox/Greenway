# Generated by Django 3.2 on 2021-04-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210411_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='greenwayuser',
            name='ReferralCode',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
