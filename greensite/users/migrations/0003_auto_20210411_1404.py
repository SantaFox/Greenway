# Generated by Django 3.1.7 on 2021-04-11 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_greenwayuser_managingpartner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greenwayuser',
            name='ManagingPartner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]