# Generated by Django 3.0.6 on 2020-05-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_gallery', verbose_name='image')),
            ],
            options={
                'verbose_name': 'service_gallery',
                'verbose_name_plural': 'service_galleries',
                'db_table': 'service_galleries',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='service_thumbnail', verbose_name='thumbnail')),
                ('slug', models.CharField(max_length=255, verbose_name='slug')),
                ('images', models.ManyToManyField(blank=True, related_name='service_gallery', to='service.ServiceGallery', verbose_name='images')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'db_table': 'services',
            },
        ),
    ]
