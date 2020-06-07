# Generated by Django 3.0.6 on 2020-06-07 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_auto_20200530_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='seo_description',
            field=models.TextField(blank=True, null=True, verbose_name='seo_description'),
        ),
        migrations.AddField(
            model_name='service',
            name='seo_title',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='seo_title'),
        ),
    ]