# Generated by Django 3.0.6 on 2020-05-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_doctor_join_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='thumbnail',
            field=models.ImageField(upload_to='doctor_thumbnail', verbose_name='thumbnail'),
        ),
    ]
