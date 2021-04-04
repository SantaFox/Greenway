# Generated by Django 3.1.7 on 2021-04-04 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0023_auto_20210404_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
                ('Product', models.ManyToManyField(to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='TagInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
                ('Language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.language')),
                ('Tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.tag')),
            ],
            options={
                'verbose_name_plural': 'Tags Info',
            },
        ),
        migrations.AddConstraint(
            model_name='taginfo',
            constraint=models.UniqueConstraint(fields=('Tag', 'Language'), name='unique_TagInfo'),
        ),
    ]
