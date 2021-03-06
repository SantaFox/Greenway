# Generated by Django 3.1.7 on 2021-04-06 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ledger', '0004_auto_20210406_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Phone', models.CharField(blank=True, max_length=50)),
                ('Email', models.CharField(blank=True, max_length=50)),
                ('Telegram', models.CharField(blank=True, max_length=50)),
                ('Facebook', models.CharField(blank=True, max_length=50)),
                ('Memo', models.TextField(blank=True)),
                ('IsSupplier', models.BooleanField(default=False)),
                ('IsCustomer', models.BooleanField(default=False)),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Counterparty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ledger.counterparty'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='counterparty',
            constraint=models.UniqueConstraint(fields=('User', 'Name'), name='unique_Counterparty'),
        ),
    ]
