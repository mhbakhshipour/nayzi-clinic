# Generated by Django 3.0.6 on 2020-06-21 10:14

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_service_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='content',
            field=froala_editor.fields.FroalaField(default='test'),
            preserve_default=False,
        ),
    ]
