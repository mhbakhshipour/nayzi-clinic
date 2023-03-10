# Generated by Django 3.0.6 on 2020-08-15 10:12

from django.db import migrations, models
import froala_editor.fields


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
                ('description', models.TextField(verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
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
                ('title', models.CharField(max_length=255, unique=True, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('content', froala_editor.fields.FroalaField()),
                ('seo_title', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title')),
                ('seo_description', models.TextField(blank=True, null=True, verbose_name='seo_description')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='service_thumbnail', verbose_name='thumbnail')),
                ('slug', models.CharField(max_length=255, unique=True, verbose_name='slug')),
                ('order', models.SmallIntegerField(unique=True, verbose_name='order')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('images', models.ManyToManyField(blank=True, related_name='service_gallery', to='service.ServiceGallery', verbose_name='images')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
                'db_table': 'services',
            },
        ),
    ]
