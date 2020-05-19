# Generated by Django 3.0.6 on 2020-05-19 10:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='thumbnail',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='user_thumbnail', verbose_name='thumbnail'),
            preserve_default=False,
        ),
    ]
