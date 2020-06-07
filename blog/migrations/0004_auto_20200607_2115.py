# Generated by Django 3.0.6 on 2020-06-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200530_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='seo_description',
            field=models.TextField(blank=True, null=True, verbose_name='seo_description'),
        ),
        migrations.AddField(
            model_name='blog',
            name='seo_title',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='seo_description',
            field=models.TextField(blank=True, null=True, verbose_name='seo_description'),
        ),
        migrations.AddField(
            model_name='blogcategory',
            name='seo_title',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title'),
        ),
    ]
