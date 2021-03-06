# Generated by Django 3.2.2 on 2021-05-13 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0040_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slug', models.SlugField()),
                ('Image', models.ImageField(upload_to='carousel/')),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarouselInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Header', models.CharField(max_length=255)),
                ('Text', models.CharField(max_length=255)),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Carousels Info',
            },
        ),
        migrations.CreateModel(
            name='Featurette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Slug', models.SlugField()),
                ('Image', models.ImageField(upload_to='featurette/')),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturetteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Header', models.CharField(max_length=255)),
                ('Text', models.CharField(max_length=255)),
                ('TimestampCreated', models.DateTimeField(auto_now_add=True)),
                ('TimestampModified', models.DateTimeField(auto_now=True)),
                ('Featurette', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='showcase.featurette')),
                ('Language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.language')),
            ],
            options={
                'verbose_name_plural': 'Featurettes Info',
            },
        ),
        migrations.AddConstraint(
            model_name='featurette',
            constraint=models.UniqueConstraint(fields=('Slug',), name='unique_Featurette'),
        ),
        migrations.AddField(
            model_name='carouselinfo',
            name='Carousel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='showcase.carousel'),
        ),
        migrations.AddField(
            model_name='carouselinfo',
            name='Language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.language'),
        ),
        migrations.AddConstraint(
            model_name='carousel',
            constraint=models.UniqueConstraint(fields=('Slug',), name='unique_Carousel'),
        ),
        migrations.AddConstraint(
            model_name='featuretteinfo',
            constraint=models.UniqueConstraint(fields=('Featurette', 'Language'), name='unique_FeaturetteInfo'),
        ),
        migrations.AddConstraint(
            model_name='carouselinfo',
            constraint=models.UniqueConstraint(fields=('Carousel', 'Language'), name='unique_CarouselInfo'),
        ),
    ]
