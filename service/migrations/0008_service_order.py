# Generated by Django 3.0.6 on 2020-06-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_auto_20200607_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='order',
            field=models.SmallIntegerField(default=0, max_length=4, verbose_name='order'),
            preserve_default=False,
        ),
    ]
